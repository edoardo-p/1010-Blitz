import json
import random
from typing import Generator

import gymnasium as gym
import numpy as np
from scipy.ndimage import label

from .piece import Piece
from .tile import Tile

State = tuple[list[list[Tile]], Piece]
Outcome = tuple[State, int, bool]


class Game1010(gym.Env):
    def __init__(self, board_size: int = 10, max_pieces: int = 3, seed=None):
        self.board_size = board_size
        self.max_pieces = max_pieces

        # https://gymnasium.farama.org/introduction/create_custom_env/
        # TODO implement self.observation_space
        # TODO implement self.action_space

        with open(r".\backend\vectors.json", "r") as f:
            self._piece_vectors = json.load(f)

        random.seed(seed)

    def reset(self, seed=None) -> State:
        super().reset(seed=seed)

        self._tiles = [
            [Tile() for _ in range(self.board_size)] for _ in range(self.board_size)
        ]
        self._grid_mask = np.zeros((self.board_size, self.board_size), dtype=int)
        self.score = 0
        self.pieces = self._generate_pieces()
        return self._tiles, self.pieces[0]

    def step(self, piece_idx: int, row: int, col: int) -> Outcome:
        if piece_idx >= len(self.pieces):
            return (self._tiles, self.pieces[0]), -1000, False

        piece = self.pieces[piece_idx]
        if not self._check_valid(row, col, piece):
            return (self._tiles, self.pieces[0]), -1000, False

        curr_score = self.score
        for tile_col, tile_row in piece.squares_pos:
            self._tiles[row + tile_row][col + tile_col].update(piece.color)
            self._grid_mask[row + tile_row][col + tile_col] = 1
        self._clear_lines()
        self.score += len(piece.squares_pos)

        self.pieces.remove(piece)
        if not self.pieces:
            self.pieces = self._generate_pieces()

        done = not any(self.get_moves())
        no_holes_reward = self._reward_large_sections(self._grid_mask)
        reward = self.score - curr_score + no_holes_reward
        if done:
            reward = -5000
        return (self._tiles, self.pieces[0]), reward, done

    def get_moves(self) -> Generator[tuple[Piece, int, int], None, None]:
        for tile, row, col in self.get_tiles_and_coords():
            if not tile.empty:
                continue

            for piece in self.pieces:
                if piece and self._check_valid(row, col, piece):
                    yield piece, row, col

    def get_tiles_and_coords(self) -> Generator[tuple[Tile, int, int], None, None]:
        for i, row in enumerate(self._tiles):
            for j, tile in enumerate(row):
                yield tile, i, j

    def _generate_pieces(self) -> list[Piece]:
        pieces = []
        for _ in range(self.max_pieces):
            piece = random.choice(self._piece_vectors)
            pieces.append(Piece(piece["pos"], piece["color"]))
        return pieces

    def _check_valid(self, row: int, col: int, piece: Piece) -> bool:
        return all(
            0 <= row + tile_row < self.board_size
            and 0 <= col + tile_col < self.board_size
            and self._tiles[row + tile_row][col + tile_col].empty
            for tile_col, tile_row in piece.squares_pos
        )

    def _clear_lines(self) -> None:
        lines = 0

        for row_num in range(self.board_size):
            row = self._get_row(row_num)
            if not any(tile.empty for tile in row):
                lines += 1
                for tile in row:
                    tile.clear()

        for col_num in range(self.board_size):
            col = self._get_col(col_num)
            if not any(tile.empty for tile in self._get_col(col_num)):
                lines += 1
                for tile in col:
                    tile.clear()

        self.score += 5 * lines * (lines + 1)

    def _reward_large_sections(self, matrix: np.ndarray) -> int:
        """
        Calculate a reward for larger contiguous sections of ones in a binary 2D matrix.

        Args:
            matrix (np.ndarray): A binary 2D matrix (values are 0 or 1).

        Returns:
            float: The reward based on the size of contiguous sections of ones.
        """
        # Label connected components of ones
        labeled_matrix, _ = label(matrix)

        # Calculate the size of each connected component
        component_sizes = np.bincount(labeled_matrix.ravel())[1:]
        reward = sum(size**2 for size in component_sizes)

        return reward

    def _get_row(self, row: int) -> list[Tile]:
        return self._tiles[row]

    def _get_col(self, col: int) -> list[Tile]:
        return [row[col] for row in self._tiles]
