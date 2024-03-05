import copy
from typing import Tuple

import numpy as np
import torch
from secretflow.ml.nn.fl.backend.torch.fl_base import BaseTorchModel
from secretflow.ml.nn.fl.strategy_dispatcher import register_strategy


class FedBN(BaseTorchModel):
    def update_weights_without_bn(self, weights):
        """
        Update model weights, but exclude Batch Normalization (BN) layers.
        Args:
            weights: global weight from params server
        """
        state_dict = (
            self.model.state_dict()
        )  # Get the state dictionary of the current model
        weights_dict = {}

        for k, v in zip(state_dict.keys(), weights):
            if 'bn' not in k:  # Check if the key is not a BN layer
                weights_dict[k] = torch.Tensor(np.copy(v))

        # Only load weights for layers that are not BN layers
        state_dict.update(weights_dict)
        self.model.load_state_dict(state_dict)

    def train_step(
        self,
        weights: np.ndarray,
        cur_steps: int,
        train_steps: int,
        **kwargs,
    ) -> Tuple[np.ndarray, int]:
        """Accept ps model params, then do local train

        Args:
            weights: global weight from params server
            cur_steps: current train step
            train_steps: local training steps
            kwargs: strategy-specific parameters
        Returns:
            Parameters after local training
        """
        assert self.model is not None, "Model cannot be none, please give model define"
        self.model.train()
        refresh_data = kwargs.get("refresh_data", False)
        if refresh_data:
            self._reset_data_iter()
        if weights is not None:
            self.update_weights_without_bn(weights)
        num_sample = 0
        dp_strategy = kwargs.get('dp_strategy', None)
        logs = {}

        for _ in range(train_steps):
            self.optimizer.zero_grad()

            x, y, s_w = self.next_batch()
            num_sample += x.shape[0]
            y_pred = self.model(x)

            # do back propagation
            loss = self.loss(y_pred, y)
            loss.backward()
            self.optimizer.step()
            for m in self.metrics:
                m.update(y_pred.cpu(), y.cpu())
        loss_value = loss.item()
        logs['train-loss'] = loss_value

        self.logs = self.transform_metrics(logs)
        self.wrapped_metrics.extend(self.wrap_local_metrics())
        self.epoch_logs = copy.deepcopy(self.logs)

        state_dict = self.model.state_dict()
        weights_list = []
        # Return weights without BN
        for k, v in state_dict.items():
            if "bn" not in k:
                weights_list.append(v.cpu().numpy())

        weights_list = [e.copy() for e in weights_list]
        model_weights = weights_list

        # DP operation
        if dp_strategy is not None:
            if dp_strategy.model_gdp is not None:
                model_weights = dp_strategy.model_gdp(model_weights)
        return model_weights, num_sample

    def apply_weights(self, weights):
        """Accept ps model params, then update local model

        Args:
            weights: global weight from params server
        """
        if weights is not None:
            self.update_weights_without_bn(weights)


@register_strategy(strategy_name='fed_bn', backend='torch')
class PYUFedBN(FedBN):
    pass