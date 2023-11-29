import os

import numpy as np
import torch
import torch.nn as nn

from backend.custom_env import Game1010
from .piece import Piece

Action = tuple[int, int, Piece]


class _Agent:
    def __init__(self) -> None:
        pass

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


class Agent:
    def __init__(
        self,
        num_actions,
        state_size,
        alpha=0.001,
        gamma=0.99,
        epsilon=0.1,
        memory_size=1000000,
        net_layers=(100, 64, 32, 16),
        batch_size=16,
        load_from_file=False,
        verbose=False,
    ):
        self.state_shape = (state_size, state_size)
        self.actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.net_layers = net_layers
        self.batch_size = batch_size
        self.memory_size = memory_size
        self.verbose = verbose

        self.memory = []

        self.checkpoint_path = "model_data/cp.ckpt"
        self.checkpoint_dir = os.path.dirname(self.checkpoint_path)

        self.build_neural_net(load_from_file)
        self.optimizer = torch.optim.Adam(self.q_net.parameters(), lr=self.alpha)
        self.loss = nn.MSELoss()

    def build_neural_net(self, load_from_net):
        self.q_net = nn.Sequential()
        for num_inputs, num_outputs in zip(self.net_layers[:-1], self.net_layers[1:]):
            self.q_net.append(nn.Linear(num_inputs, num_outputs))
            self.q_net.append(nn.ReLU())
        # self.q_net.append(nn.Flatten())
        self.q_net.append(nn.Linear(self.net_layers[-1], 10))  # TODO parametrize

        if load_from_net:
            try:
                self.q_net.load_state_dict(torch.load(self.checkpoint_path))
                self.q_net.load_weights(self.checkpoint_path)
            except ValueError:
                print(
                    f"No weight data found at {self.checkpoint_path}, building new agent"
                )
        if self.verbose:
            print(self.q_net)
        return

    def choose_action(self, state, random_choice=False) -> int:
        vector = self._state_to_tensor(state)
        # Chooses random action
        if random_choice or np.random.uniform(0, 1) <= self.epsilon:
            return np.random.choice(self.actions)

        # Chooses best q_value action
        q_out = self.q_net(vector)
        return torch.argmax(q_out).item()

    def learn(self):
        return
        try:
            experience_sample = np.random.choice(self.memory, self.batch_size)
        except ValueError:
            return

        states = np.array([trajectory["state"] for trajectory in experience_sample])
        next_states = np.array(
            [trajectory["next_state"] for trajectory in experience_sample]
        )
        q_values = self.q_net.predict(
            next_states.reshape(self.batch_size, *self.state_shape)
        )
        target = self.q_net(states.reshape(self.batch_size, *self.state_shape)).numpy()

        for i in range(self.batch_size):
            trajectory = experience_sample[i]
            action = trajectory["action"]
            target = trajectory["reward"]
            if not trajectory["terminal"]:
                target += self.gamma * np.amax(q_values[i][:])
            target[i][action] = target

        pred = self.q_net(
            states.reshape(self.batch_size, *self.state_shape),
        )
        self.loss(pred, target).backward()
        self.optimizer.step()

    def _state_to_tensor(self, state):
        return torch.tensor(
            [0 if tile.empty else 1 for row in state for tile in row],
            dtype=torch.float32,
        )
