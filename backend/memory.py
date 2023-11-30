import random
from collections import deque
from dataclasses import dataclass

import torch


@dataclass
class Transition:
    state: torch.Tensor
    action: torch.Tensor
    next_state: torch.Tensor
    reward: torch.Tensor

    def __iter__(self):
        return iter((self.state, self.action, self.next_state, self.reward))


class ReplayMemory:
    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        """Save a transition"""
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)
