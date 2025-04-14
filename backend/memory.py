import random
from collections import deque
from dataclasses import dataclass

import torch


@dataclass
class Transition:
    state: tuple[torch.Tensor, torch.Tensor]
    action: torch.Tensor
    next_state: torch.Tensor | None
    reward: torch.Tensor


class ReplayMemory:
    def __init__(self, capacity: int):
        self.memory = deque([], maxlen=capacity)

    def push(
        self,
        state: tuple[torch.Tensor, torch.Tensor],
        action: torch.Tensor,
        next_state: torch.Tensor | None,
        reward: torch.Tensor,
    ) -> None:
        self.memory.append(Transition(state, action, next_state, reward))

    def sample(self, batch_size: int) -> list[Transition]:
        return random.sample(self.memory, batch_size)

    def __len__(self) -> int:
        return len(self.memory)
