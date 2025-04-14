import numpy as np
import torch
import torch.nn as nn

from .dqn import DQNNet
from .memory import ReplayMemory

Action = tuple[int, int, int]


class DQNAgent:
    def __init__(
        self,
        num_actions,
        state_shape,
        device,
        train=True,
        alpha=0.001,
        gamma=0.99,
        epsilon_start=0.9,
        epsilon_end=0.01,
        epsilon_decay=200,
        memory_size=25000,
        batch_size=256,
    ):
        self.actions = num_actions
        self.state_shape = state_shape
        self.device = device
        self.train = train
        self._gamma = gamma
        self._epsilon_start = epsilon_start
        self._epsilon_end = epsilon_end
        self._epsilon_decay = epsilon_decay
        self._batch_size = batch_size

        self._step = 0
        self._policy_net = DQNNet(num_actions).to(self.device)
        self._target_net = DQNNet(num_actions).to(self.device)
        self._target_net.load_state_dict(self._policy_net.state_dict())

        self._optimizer = torch.optim.AdamW(self._policy_net.parameters(), lr=alpha)
        self._memory = ReplayMemory(memory_size)

    def load(self, model_dir: str):
        self._policy_net.load_state_dict(torch.load(rf"{model_dir}\policy_net.pth"))
        self._target_net.load_state_dict(torch.load(rf"{model_dir}\target_net.pth"))

    def choose_action(self, state: torch.Tensor, piece: torch.Tensor) -> torch.Tensor:
        # Chooses random action
        if np.random.uniform(0, 1) <= self._epsilon():
            return torch.randint(self.actions, (1, 1), device=self.device)

        # Chooses best q_value action
        # piece_idx = ... (Piece -> torch.Tensor)
        return self._policy_net(state, piece).argmax().reshape(-1, 1)

    def learn(self):
        if not self.train or len(self._memory) < self._batch_size:
            return
        transitions = self._memory.sample(self._batch_size)

        # Compute a mask of non-final states and concatenate the batch elements
        # (a final state would've been the one after which simulation ended)
        non_final_mask = torch.tensor(
            [s.next_state is not None for s in transitions],
            device=self.device,
            dtype=torch.bool,
        )
        next_state_transpose = zip(
            *(s.next_state for s in transitions if s.next_state is not None)
        )
        non_final_next_states = [
            torch.cat(transpose) for transpose in next_state_transpose
        ]

        state_transpose = zip(*[t.state for t in transitions])
        state_batch = [torch.cat(transpose) for transpose in state_transpose]
        action_batch = torch.cat([t.action for t in transitions])
        reward_batch = torch.cat([t.reward for t in transitions])

        # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
        # columns of actions taken. These are the actions which would've been taken
        # for each batch state according to policy_net
        state_action_values = self._policy_net(*state_batch).gather(1, action_batch)

        # Compute V(s_{t+1}) for all next states.
        # Expected values of actions for non_final_next_states are computed based
        # on the "older" target_net; selecting their best reward with max(1).values
        # This is merged based on the mask, such that we'll have either the expected
        # state value or 0 in case the state was final.
        next_state_values = torch.zeros(self._batch_size, device=self.device)
        with torch.no_grad():
            # TODO update next_state_values using the target net but without piece information
            next_state_values[non_final_mask] = (
                self._target_net(*non_final_next_states).max(1).values
            )
        # Compute the expected Q values
        expected_state_action_values = (next_state_values * self._gamma) + reward_batch

        # Compute Huber loss
        criterion = nn.SmoothL1Loss()
        loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

        # Optimize the model
        self._optimizer.zero_grad()
        loss.backward()
        # In-place gradient clipping
        # torch.nn.utils.clip_grad_value_(self.policy_net.parameters(), 100)
        self._optimizer.step()

    def action_to_tuple(self, action: torch.Tensor) -> Action:
        piece_idx, coords = divmod(
            action.cpu().item(), self.state_shape[0] * self.state_shape[1]
        )
        row, col = divmod(coords, self.state_shape[0])
        return int(piece_idx), int(row), int(col)

    def add_memory_sample(
        self,
        state: tuple[torch.Tensor, torch.Tensor],
        action: torch.Tensor,
        next_state: tuple[torch.Tensor, torch.Tensor] | None,
        reward: torch.Tensor,
    ) -> None:
        next_state_without_piece = None if next_state is None else next_state[0]
        self._memory.push(state, action, next_state_without_piece, reward)

    def _epsilon(self) -> float:
        if not self.train:
            return self._epsilon_end
        decay = np.exp(-self._step / self._epsilon_decay)
        return self._epsilon_end + (self._epsilon_start - self._epsilon_end) * decay
