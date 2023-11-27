import os

import numpy as np
import torch
import torch.nn as nn

from frontend.constants import BOARD_SIZE
from frontend.game import Game
from frontend.piece import Piece


class _Agent:
    def __init__(self) -> None:
        pass

    def move(self, game: Game, pieces: list[Piece]):
        board = [0 if tile.empty else 1 for tile, *_ in game.get_tiles_and_coords()]
        moves = [
            self.convert_move_to_array(row, col, piece, board)
            for piece, row, col in game.get_moves(pieces)
        ]

    def convert_move_to_array(
        self, row: int, col: int, piece: Piece, board: list[int]
    ) -> list[int]:
        for tile_col, tile_row in piece.squares_pos:
            idx = (row + tile_row) * BOARD_SIZE + (col + tile_col)
            board[idx] = 1

        return board


class Agent:
    def __init__(
        self,
        action_space,
        state_size,
        state_frames,
        alpha=0.001,
        gamma=0.99,
        epsilon=0.1,
        memory_size=1000000,
        net_layers=(64, 32, 16),
        batch_size=16,
        load_from_file=False,
    ):
        super().__init__(action_space)
        self.state_shape = (state_frames, state_size, state_size)

        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.net_layers = net_layers
        self.batch_size = batch_size
        self.memory_size = memory_size

        self.memory = []

        self.checkpoint_path = "model_data/cp.ckpt"
        self.checkpoint_dir = os.path.dirname(self.checkpoint_path)

        self.build_neural_net(load_from_file)

    def build_neural_net(self, load_from_net):
        self.q_net = nn.Sequential()
        for num_inputs, num_outputs in zip(self.net_layers[:-1], self.net_layers[1:]):
            self.q_net.append(nn.Linear(num_inputs, num_outputs))
            self.q_net.append(nn.ReLU())
        self.q_net.append(nn.Flatten())
        self.q_net.append(nn.Linear(self.net_layers[-1], self.num_actions))

        if load_from_net:
            try:
                self.q_net.load_state_dict(torch.load(self.checkpoint_path))
                self.q_net.load_weights(self.checkpoint_path)
            except ValueError:
                print(
                    f"No weight data found at {self.checkpoint_path}, building new agent"
                )
        self.q_net.summary()
        return

    def choose_action(self, state, random_choice=False):
        # Chooses random action
        if random_choice or np.random.uniform(0, 1) <= self.epsilon:
            return np.random.choice(self.action_space)

        # Chooses best q_value action
        q_out = self.q_net(np.array(state).reshape(1, *self.state_shape))
        return np.argmax(q_out)

    def learn(self):
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
        prediction_target = self.q_net(
            states.reshape(self.batch_size, *self.state_shape)
        ).numpy()

        for i in range(self.batch_size):
            trajectory = experience_sample[i]
            action = trajectory["action"]
            target = trajectory["reward"]
            if not trajectory["terminal"]:
                target += self.gamma * np.amax(q_values[i][:])
            prediction_target[i][action] = target

        self.q_net.fit(
            states.reshape(self.batch_size, *self.state_shape),
            prediction_target,
            batch_size=self.batch_size,
            callbacks=[self.cp_callback],
        )

    def save_trajectory(self, state, action, reward, next_state, terminal):
        trajectory = {
            "state": state,
            "action": action,
            "reward": reward,
            "next_state": next_state,
            "terminal": terminal,
        }
        self.memory.append(trajectory)
        if len(self.memory) > self.memory_size:
            del self.memory[np.random.randint(self.memory_size - 1)]
