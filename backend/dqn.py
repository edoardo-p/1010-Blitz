import torch
import torch.nn as nn


class DQNNet(nn.Module):
    def __init__(self, net_layers: list[int], num_actions: int):
        super().__init__()

        self.q_net = nn.Sequential()
        for num_inputs, num_outputs in zip(net_layers[:-1], net_layers[1:]):
            self.q_net.append(nn.Linear(num_inputs, num_outputs))
            self.q_net.append(nn.ReLU())
        self.q_net.append(nn.Linear(net_layers[-1], num_actions))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.q_net(x)
