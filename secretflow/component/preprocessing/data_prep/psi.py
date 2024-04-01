# Copyright 2023 Ant Group Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from typing import List

from secretflow.component.component import (
    CompEvalError,
    Component,
    IoType,
    TableColParam,
)
from secretflow.component.data_utils import (
    DistDataType,
    download_files,
    extract_distdata_info,
    merge_individuals_to_vtable,
    upload_files,
)
from secretflow.device.device.spu import SPU
from secretflow.spec.v1.data_pb2 import DistData, IndividualTable, VerticalTable

psi_comp = Component(
    "psi",
    domain="data_prep",
    version="0.0.3",
    desc="PSI between two parties.",
)
psi_comp.str_attr(
    name="protocol",
    desc="PSI protocol.",
    is_list=False,
    is_optional=True,
    default_value="PROTOCOL_RR22",
    allowed_values=["PROTOCOL_RR22", "PROTOCOL_ECDH", "PROTOCOL_KKRT"],
)
psi_comp.bool_attr(
    name="disable_alignment",
    desc="It true, output is not promised to be aligned. Warning: enable this option may lead to errors in the following components. DO NOT TURN ON if you want to append other components.",
    is_list=False,
    is_optional=True,
    default_value=False,
)
psi_comp.bool_attr(
    name="skip_duplicates_check",
    desc="If true, the check of duplicated items will be skiped.",
    is_list=False,
    is_optional=True,
    default_value=False,
)
psi_comp.bool_attr(
    name="check_hash_digest",
    desc="Check if hash digest of keys from parties are equal to determine whether to early-stop.",
    is_list=False,
    is_optional=True,
    default_value=False,
)
psi_comp.party_attr(
    name="left_side", desc="Required if advanced_join_type is selected."
)
psi_comp.str_attr(
    name="join_type",
    desc="Advanced Join types allow duplicate keys.",
    is_list=False,
    is_optional=True,
    default_value="ADVANCED_JOIN_TYPE_UNSPECIFIED",
    allowed_values=[
        "ADVANCED_JOIN_TYPE_UNSPECIFIED",
        "ADVANCED_JOIN_TYPE_INNER_JOIN",
        "ADVANCED_JOIN_TYPE_LEFT_JOIN",
        "ADVANCED_JOIN_TYPE_RIGHT_JOIN",
        "ADVANCED_JOIN_TYPE_FULL_JOIN",
        "ADVANCED_JOIN_TYPE_DIFFERENCE",
    ],
)
psi_comp.str_attr(
    name="missing_value",
    desc="Missing value for some advanced join types.",
    is_list=False,
    is_optional=True,
    default_value="NA",
    allowed_values=[
        "NA",
    ],
)
psi_comp.str_attr(
    name="ecdh_curve",
    desc="Curve type for ECDH PSI.",
    is_list=False,
    is_optional=True,
    default_value="CURVE_FOURQ",
    allowed_values=["CURVE_25519", "CURVE_FOURQ", "CURVE_SM2", "CURVE_SECP256K1"],
)
psi_comp.io(
    io_type=IoType.INPUT,
    name="receiver_input",
    desc="Individual table for receiver",
    types=[DistDataType.INDIVIDUAL_TABLE],
    col_params=[
        TableColParam(
            name="key",
            desc="Column(s) used to join.",
            col_min_cnt_inclusive=1,
        )
    ],
)
psi_comp.io(
    io_type=IoType.INPUT,
    name="sender_input",
    desc="Individual table for sender",
    types=[DistDataType.INDIVIDUAL_TABLE],
    col_params=[
        TableColParam(
            name="key",
            desc="Column(s) used to join.",
            col_min_cnt_inclusive=1,
        )
    ],
)
psi_comp.io(
    io_type=IoType.OUTPUT,
    name="psi_output",
    desc="Output vertical table",
    types=[DistDataType.VERTICAL_TABLE],
)


# We would respect user-specified ids even ids are set in TableSchema.
def modify_schema(x: DistData, keys: List[str]) -> DistData:
    new_x = DistData()
    new_x.CopyFrom(x)
    if len(keys) == 0:
        return new_x
    assert x.type == "sf.table.individual"
    imeta = IndividualTable()
    assert x.meta.Unpack(imeta)

    new_meta = IndividualTable()
    names = []
    types = []

    # copy current ids to features and clean current ids.
    for i, t in zip(list(imeta.schema.ids), list(imeta.schema.id_types)):
        names.append(i)
        types.append(t)

    for f, t in zip(list(imeta.schema.features), list(imeta.schema.feature_types)):
        names.append(f)
        types.append(t)

    for k in keys:
        if k not in names:
            raise CompEvalError(f"key {k} is not found as id or feature.")

    for n, t in zip(names, types):
        if n in keys:
            new_meta.schema.ids.append(n)
            new_meta.schema.id_types.append(t)
        else:
            new_meta.schema.features.append(n)
            new_meta.schema.feature_types.append(t)

    new_meta.schema.labels.extend(list(imeta.schema.labels))
    new_meta.schema.label_types.extend(list(imeta.schema.label_types))
    new_meta.line_count = imeta.line_count

    new_x.meta.Pack(new_meta)

    return new_x


@psi_comp.eval_fn
def two_party_balanced_psi_eval_fn(
    *,
    ctx,
    protocol,
    disable_alignment,
    skip_duplicates_check,
    check_hash_digest,
    ecdh_curve,
    join_type,
    left_side,
    missing_value,
    receiver_input,
    receiver_input_key,
    sender_input,
    sender_input_key,
    psi_output,
):
    receiver_path_format = extract_distdata_info(receiver_input)
    assert len(receiver_path_format) == 1
    receiver_party = list(receiver_path_format.keys())[0]
    sender_path_format = extract_distdata_info(sender_input)
    sender_party = list(sender_path_format.keys())[0]

    assert left_side[0] in [
        receiver_party,
        sender_party,
    ], f'left side {left_side[0]} is invalid.'

    assert missing_value == 'NA'

    if ctx.spu_configs is None or len(ctx.spu_configs) == 0:
        raise CompEvalError("spu config is not found.")
    if len(ctx.spu_configs) > 1:
        raise CompEvalError("only support one spu")
    spu_config = next(iter(ctx.spu_configs.values()))

    input_path = {
        receiver_party: os.path.join(
            ctx.data_dir, receiver_path_format[receiver_party].uri
        ),
        sender_party: os.path.join(ctx.data_dir, sender_path_format[sender_party].uri),
    }
    output_path = {
        receiver_party: os.path.join(ctx.data_dir, psi_output),
        sender_party: os.path.join(ctx.data_dir, psi_output),
    }

    import logging

    logging.warning(spu_config)

    spu = SPU(spu_config["cluster_def"], spu_config["link_desc"])

    uri = {
        receiver_party: receiver_path_format[receiver_party].uri,
        sender_party: sender_path_format[sender_party].uri,
    }

    with ctx.tracer.trace_io():
        download_files(ctx, uri, input_path)

    with ctx.tracer.trace_running():
        report = spu.psi(
            keys={receiver_party: receiver_input_key, sender_party: sender_input_key},
            input_path=input_path,
            output_path=output_path,
            receiver=receiver_party,
            broadcast_result=True,
            protocol=protocol,
            ecdh_curve=ecdh_curve,
            advanced_join_type=join_type,
            left_side=(
                'ROLE_RECEIVER' if left_side[0] == receiver_party else 'ROLE_SENDER'
            ),
            skip_duplicates_check=skip_duplicates_check,
            disable_alignment=disable_alignment,
            check_hash_digest=check_hash_digest,
        )

    with ctx.tracer.trace_io():
        upload_files(
            ctx, {receiver_party: psi_output, sender_party: psi_output}, output_path
        )

    output_db = DistData(
        name=psi_output,
        type=str(DistDataType.VERTICAL_TABLE),
        system_info=receiver_input.system_info,
        data_refs=[
            DistData.DataRef(
                uri=psi_output,
                party=receiver_party,
                format="csv",
            ),
            DistData.DataRef(
                uri=psi_output,
                party=sender_party,
                format="csv",
            ),
        ],
    )

    output_db = merge_individuals_to_vtable(
        [
            modify_schema(receiver_input, receiver_input_key),
            modify_schema(sender_input, sender_input_key),
        ],
        output_db,
    )
    vmeta = VerticalTable()
    assert output_db.meta.Unpack(vmeta)
    vmeta.line_count = report[0]['intersection_count']
    output_db.meta.Pack(vmeta)

    return {"psi_output": output_db}
