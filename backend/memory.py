import random
from collections import deque
from dataclasses import dataclass


@dataclass
class Transition:
    state: list
    action: int
    next_state: list
    reward: float


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
