# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: secretflow/spec/v1/data.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dsecretflow/spec/v1/data.proto\x12\x12secretflow.spec.v1\x1a\x19google/protobuf/any.proto\"A\n\nSystemInfo\x12\x0b\n\x03\x61pp\x18\x01 \x01(\t\x12&\n\x08\x61pp_meta\x18\x02 \x01(\x0b\x32\x14.google.protobuf.Any\"\xcd\x02\n\rStorageConfig\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x41\n\x08local_fs\x18\x02 \x01(\x0b\x32/.secretflow.spec.v1.StorageConfig.LocalFSConfig\x12\x36\n\x02s3\x18\x03 \x01(\x0b\x32*.secretflow.spec.v1.StorageConfig.S3Config\x1a\x1b\n\rLocalFSConfig\x12\n\n\x02wd\x18\x01 \x01(\t\x1a\x95\x01\n\x08S3Config\x12\x10\n\x08\x65ndpoint\x18\x01 \x01(\t\x12\x0e\n\x06\x62ucket\x18\x02 \x01(\t\x12\x0e\n\x06prefix\x18\x03 \x01(\t\x12\x15\n\raccess_key_id\x18\x04 \x01(\t\x12\x19\n\x11\x61\x63\x63\x65ss_key_secret\x18\x05 \x01(\t\x12\x14\n\x0cvirtual_host\x18\x06 \x01(\x08\x12\x0f\n\x07version\x18\x07 \x01(\t\"\xef\x01\n\x08\x44istData\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x33\n\x0bsystem_info\x18\x03 \x01(\x0b\x32\x1e.secretflow.spec.v1.SystemInfo\x12\"\n\x04meta\x18\x04 \x01(\x0b\x32\x14.google.protobuf.Any\x12\x37\n\tdata_refs\x18\x05 \x03(\x0b\x32$.secretflow.spec.v1.DistData.DataRef\x1a\x35\n\x07\x44\x61taRef\x12\x0b\n\x03uri\x18\x01 \x01(\t\x12\r\n\x05party\x18\x02 \x01(\t\x12\x0e\n\x06\x66ormat\x18\x03 \x01(\t\"U\n\rVerticalTable\x12\x30\n\x07schemas\x18\x01 \x03(\x0b\x32\x1f.secretflow.spec.v1.TableSchema\x12\x12\n\nline_count\x18\x02 \x01(\x03\"V\n\x0fIndividualTable\x12/\n\x06schema\x18\x01 \x01(\x0b\x32\x1f.secretflow.spec.v1.TableSchema\x12\x12\n\nline_count\x18\x02 \x01(\x03\"z\n\x0bTableSchema\x12\x0b\n\x03ids\x18\x01 \x03(\t\x12\x10\n\x08\x66\x65\x61tures\x18\x02 \x03(\t\x12\x0e\n\x06labels\x18\x03 \x03(\t\x12\x10\n\x08id_types\x18\x04 \x03(\t\x12\x15\n\rfeature_types\x18\x05 \x03(\t\x12\x13\n\x0blabel_types\x18\x06 \x03(\tB%\n\x16\x63om.secretflow.spec.v1B\tDataProtoP\x01\x62\x06proto3')



_SYSTEMINFO = DESCRIPTOR.message_types_by_name['SystemInfo']
_STORAGECONFIG = DESCRIPTOR.message_types_by_name['StorageConfig']
_STORAGECONFIG_LOCALFSCONFIG = _STORAGECONFIG.nested_types_by_name['LocalFSConfig']
_STORAGECONFIG_S3CONFIG = _STORAGECONFIG.nested_types_by_name['S3Config']
_DISTDATA = DESCRIPTOR.message_types_by_name['DistData']
_DISTDATA_DATAREF = _DISTDATA.nested_types_by_name['DataRef']
_VERTICALTABLE = DESCRIPTOR.message_types_by_name['VerticalTable']
_INDIVIDUALTABLE = DESCRIPTOR.message_types_by_name['IndividualTable']
_TABLESCHEMA = DESCRIPTOR.message_types_by_name['TableSchema']
SystemInfo = _reflection.GeneratedProtocolMessageType('SystemInfo', (_message.Message,), {
  'DESCRIPTOR' : _SYSTEMINFO,
  '__module__' : 'secretflow.spec.v1.data_pb2'
  # @@protoc_insertion_point(class_scope:secretflow.spec.v1.SystemInfo)
  })
_sym_db.RegisterMessage(SystemInfo)

StorageConfig = _reflection.GeneratedProtocolMessageType('StorageConfig', (_message.Message,), {

  'LocalFSConfig' : _reflection.GeneratedProtocolMessageType('LocalFSConfig', (_message.Message,), {
    'DESCRIPTOR' : _STORAGECONFIG_LOCALFSCONFIG,
    '__module__' : 'secretflow.spec.v1.data_pb2'
    # @@protoc_insertion_point(class_scope:secretflow.spec.v1.StorageConfig.LocalFSConfig)
    })
  ,

  'S3Config' : _reflection.GeneratedProtocolMessageType('S3Config', (_message.Message,), {
    'DESCRIPTOR' : _STORAGECONFIG_S3CONFIG,
    '__module__' : 'secretflow.spec.v1.data_pb2'
    # @@protoc_insertion_point(class_scope:secretflow.spec.v1.StorageConfig.S3Config)
    })
  ,
  'DESCRIPTOR' : _STORAGECONFIG,
  '__module__' : 'secretflow.spec.v1.data_pb2'
  # @@protoc_insertion_point(class_scope:secretflow.spec.v1.StorageConfig)
  })
_sym_db.RegisterMessage(StorageConfig)
_sym_db.RegisterMessage(StorageConfig.LocalFSConfig)
_sym_db.RegisterMessage(StorageConfig.S3Config)

DistData = _reflection.GeneratedProtocolMessageType('DistData', (_message.Message,), {

  'DataRef' : _reflection.GeneratedProtocolMessageType('DataRef', (_message.Message,), {
    'DESCRIPTOR' : _DISTDATA_DATAREF,
    '__module__' : 'secretflow.spec.v1.data_pb2'
    # @@protoc_insertion_point(class_scope:secretflow.spec.v1.DistData.DataRef)
    })
  ,
  'DESCRIPTOR' : _DISTDATA,
  '__module__' : 'secretflow.spec.v1.data_pb2'
  # @@protoc_insertion_point(class_scope:secretflow.spec.v1.DistData)
  })
_sym_db.RegisterMessage(DistData)
_sym_db.RegisterMessage(DistData.DataRef)

VerticalTable = _reflection.GeneratedProtocolMessageType('VerticalTable', (_message.Message,), {
  'DESCRIPTOR' : _VERTICALTABLE,
  '__module__' : 'secretflow.spec.v1.data_pb2'
  # @@protoc_insertion_point(class_scope:secretflow.spec.v1.VerticalTable)
  })
_sym_db.RegisterMessage(VerticalTable)

IndividualTable = _reflection.GeneratedProtocolMessageType('IndividualTable', (_message.Message,), {
  'DESCRIPTOR' : _INDIVIDUALTABLE,
  '__module__' : 'secretflow.spec.v1.data_pb2'
  # @@protoc_insertion_point(class_scope:secretflow.spec.v1.IndividualTable)
  })
_sym_db.RegisterMessage(IndividualTable)

TableSchema = _reflection.GeneratedProtocolMessageType('TableSchema', (_message.Message,), {
  'DESCRIPTOR' : _TABLESCHEMA,
  '__module__' : 'secretflow.spec.v1.data_pb2'
  # @@protoc_insertion_point(class_scope:secretflow.spec.v1.TableSchema)
  })
_sym_db.RegisterMessage(TableSchema)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\026com.secretflow.spec.v1B\tDataProtoP\001'
  _SYSTEMINFO._serialized_start=80
  _SYSTEMINFO._serialized_end=145
  _STORAGECONFIG._serialized_start=148
  _STORAGECONFIG._serialized_end=481
  _STORAGECONFIG_LOCALFSCONFIG._serialized_start=302
  _STORAGECONFIG_LOCALFSCONFIG._serialized_end=329
  _STORAGECONFIG_S3CONFIG._serialized_start=332
  _STORAGECONFIG_S3CONFIG._serialized_end=481
  _DISTDATA._serialized_start=484
  _DISTDATA._serialized_end=723
  _DISTDATA_DATAREF._serialized_start=670
  _DISTDATA_DATAREF._serialized_end=723
  _VERTICALTABLE._serialized_start=725
  _VERTICALTABLE._serialized_end=810
  _INDIVIDUALTABLE._serialized_start=812
  _INDIVIDUALTABLE._serialized_end=898
  _TABLESCHEMA._serialized_start=900
  _TABLESCHEMA._serialized_end=1022
# @@protoc_insertion_point(module_scope)
