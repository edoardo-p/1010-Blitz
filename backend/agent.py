from abc import ABC, abstractmethod

import numpy as np
import torch
import torch.nn as nn

from .custom_env import Game1010
from .dqn import DQNNet
from .memory import ReplayMemory, Transition
from .piece import Piece

Action = tuple[int, int, int]


class Agent(ABC):
    def __init__(self, state_shape: tuple[int, ...], num_actions: int):
        self.state_shape = state_shape
        self.num_actions = num_actions

    @abstractmethod
    def choose_action(self, state: np.ndarray) -> Action:
        pass

    @abstractmethod
    def learn(self, state: np.ndarray, action: Action, reward: float) -> None:
        pass


class RandomAgent:
    def move(self, game: Game1010):
        board = [0 if tile.empty else 1 for tile, *_ in game.get_tiles_and_coords()]
        moves = [
            self.convert_move_to_array(row, col, piece, board)
            for piece, row, col in game.get_moves()
        ]

    def convert_move_to_array(
        self, row: int, col: int, piece: Piece, board: list[int]
    ) -> list[int]:
        for tile_col, tile_row in piece.squares_pos:
            idx = (row + tile_row) * 10 + (col + tile_col)
            board[idx] = 1

        return board


class DQNAgent:
    def __init__(
        self,
        num_actions,
        state_shape,
        alpha=0.001,
        gamma=0.99,
        epsilon_start=0.1,
        epsilon_end=0.1,
        epsilon_decay=0.1,
        memory_size=1000000,
        batch_size=16,
    ):
        self.state_shape = state_shape
        self.actions = num_actions
        self.gamma = gamma
        self.epsilon_start = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        layers = [state_shape[0] * state_shape[1], 128, 256, num_actions]

        self.policy_net = DQNNet(layers, num_actions).to(self.device)
        self.target_net = DQNNet(layers, num_actions).to(self.device)
        self.target_net.load_state_dict(self.policy_net.state_dict())

        self.optimizer = torch.optim.AdamW(self.policy_net.parameters(), lr=alpha)
        self.memory = ReplayMemory(memory_size)

    def choose_action(self, state, steps, random_choice=False) -> Action:
        # Chooses random action
        if random_choice or np.random.uniform(0, 1) <= self._epsilon(steps):
            action = np.random.choice(self.actions)

        # Chooses best q_value action
        else:
            vector = self._state_to_tensor(state)
            action = self.policy_net(vector).max(1).indices.view(1, 1)

        piece_idx, coords = divmod(action, self.state_shape[0] * self.state_shape[1])
        row, col = divmod(coords, self.state_shape[0])
        return piece_idx, row, col

    def learn(self):
        if len(self.memory) < self.batch_size:
            return
        transitions = self.memory.sample(self.batch_size)
        # Transpose the batch (see https://stackoverflow.com/a/19343/3343043 for
        # detailed explanation). This converts batch-array of Transitions
        # to Transition of batch-arrays.
        batch = Transition(*zip(*transitions))

        # Compute a mask of non-final states and concatenate the batch elements
        # (a final state would've been the one after which simulation ended)
        non_final_mask = torch.tensor(
            tuple(map(lambda s: s is not None, batch.next_state)),
            device=self.device,
            dtype=torch.bool,
        )
        non_final_next_states = torch.cat(
            [s for s in batch.next_state if s is not None]
        )
        state_batch = torch.cat(batch.state)
        action_batch = torch.cat(batch.action)
        reward_batch = torch.cat(batch.reward)

        # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
        # columns of actions taken. These are the actions which would've been taken
        # for each batch state according to policy_net
        state_action_values = self.policy_net(state_batch).gather(1, action_batch)

        # Compute V(s_{t+1}) for all next states.
        # Expected values of actions for non_final_next_states are computed based
        # on the "older" target_net; selecting their best reward with max(1).values
        # This is merged based on the mask, such that we'll have either the expected
        # state value or 0 in case the state was final.
        next_state_values = torch.zeros(self.batch_size, device=self.device)
        with torch.no_grad():
            next_state_values[non_final_mask] = (
                self.target_net(non_final_next_states).max(1).values
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

    def _state_to_tensor(self, state):
        return torch.tensor(
            [0 if tile.empty else 1 for row in state for tile in row],
            dtype=torch.float32,
        )

    def _epsilon(self, steps: int) -> float:
        decay = np.exp(-steps / self.epsilon_decay)
        return self.epsilon_end + (self.epsilon_start - self.epsilon_end) * decay
