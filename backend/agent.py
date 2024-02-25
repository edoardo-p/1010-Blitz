import numpy as np
import torch
import torch.nn as nn

from .dqn import DQNNet
from .memory import ReplayMemory, Transition

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
        self.gamma = gamma
        self.epsilon_start = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size

        self.step = 0
        self.policy_net = DQNNet(num_actions).to(self.device)
        self.target_net = DQNNet(num_actions).to(self.device)
        self.target_net.load_state_dict(self.policy_net.state_dict())

        self.optimizer = torch.optim.AdamW(self.policy_net.parameters(), lr=alpha)
        self.memory = ReplayMemory(memory_size)

    def load(self, model_dir: str):
        self.policy_net.load_state_dict(torch.load(rf"{model_dir}\policy_net.pth"))
        self.target_net.load_state_dict(torch.load(rf"{model_dir}\target_net.pth"))

    def choose_action(self, state: torch.Tensor, piece: torch.Tensor) -> torch.Tensor:
        # Chooses random action
        if np.random.uniform(0, 1) <= self._epsilon():
            return torch.randint(self.actions, (1, 1), device=self.device)

        # Chooses best q_value action
        # piece_idx = ... (Piece -> torch.Tensor)
        return self.policy_net(state, piece).argmax().reshape(-1, 1)

    def learn(self):
        if not self.train or len(self.memory) < self.batch_size:
            return
        transitions = self.memory.sample(self.batch_size)
        batch = Transition(*zip(*transitions))

        # Compute a mask of non-final states and concatenate the batch elements
        # (a final state would've been the one after which simulation ended)
        non_final_mask = torch.tensor(
            [s is not None for s in batch.next_state],
            device=self.device,
            dtype=torch.bool,
        )
        next_state_transpose = zip(*(s for s in batch.next_state if s is not None))
        non_final_next_states = [
            torch.cat(transpose) for transpose in next_state_transpose
        ]

        state_transpose = zip(*batch.state)
        state_batch = [torch.cat(transpose) for transpose in state_transpose]
        action_batch = torch.cat(batch.action)
        reward_batch = torch.cat(batch.reward)

        # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
        # columns of actions taken. These are the actions which would've been taken
        # for each batch state according to policy_net
        state_action_values = self.policy_net(*state_batch).gather(1, action_batch)

        # Compute V(s_{t+1}) for all next states.
        # Expected values of actions for non_final_next_states are computed based
        # on the "older" target_net; selecting their best reward with max(1).values
        # This is merged based on the mask, such that we'll have either the expected
        # state value or 0 in case the state was final.
        next_state_values = torch.zeros(self.batch_size, device=self.device)
        with torch.no_grad():
            next_state_values[non_final_mask] = (
                self.target_net(*non_final_next_states).max(1).values
            )
        # Compute the expected Q values
        expected_state_action_values = (next_state_values * self.gamma) + reward_batch

        # Compute Huber loss
        criterion = nn.SmoothL1Loss()
        loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

        # Optimize the model
        self.optimizer.zero_grad()
        loss.backward()
        # In-place gradient clipping
        # torch.nn.utils.clip_grad_value_(self.policy_net.parameters(), 100)
        self.optimizer.step()

    def action_to_tuple(self, action: torch.Tensor) -> Action:
        piece_idx, coords = divmod(
            action.cpu().item(), self.state_shape[0] * self.state_shape[1]
        )
        row, col = divmod(coords, self.state_shape[0])
        return int(piece_idx), int(row), int(col)

    def _epsilon(self) -> float:
        if not self.train:
            return self.epsilon_end
        decay = np.exp(-self.step / self.epsilon_decay)
        return self.epsilon_end + (self.epsilon_start - self.epsilon_end) * decay
