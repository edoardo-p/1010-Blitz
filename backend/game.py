import json
import random

from .piece import Piece
from .tile import Tile


class Game:
    def __init__(self, board_size: int):
        self.score = 0
        self.board_size = board_size

        with open(r".\backend\vectors.json", "r") as f:
            self._piece_vectors = json.load(f)
        del f

        self.pieces = self._generate_pieces()
        self._tiles = [[Tile() for _ in range(board_size)] for _ in range(board_size)]

    def update(self, row: int, col: int, piece: Piece) -> bool:
        if not self._check_valid(row, col, piece):
            return False

        for tile_col, tile_row in piece.squares_pos:
            self._tiles[row + tile_row][col + tile_col].update(piece.color)
        self._clear_lines()
        self.score += len(piece.squares_pos)
        return True

    def has_lost(self) -> bool:
        return not any(self.get_moves())

    def get_piece_at_slot(self, slot: int) -> Piece | None:
        if slot >= len(self.pieces):
            return None

        piece = self.pieces.pop(slot)
        if not self.pieces:
            self.pieces = self._generate_pieces()
        return piece

    def get_moves(self):
        for tile, row, col in self.get_tiles_and_coords():
            if not tile.empty:
                continue

            for piece in self.pieces:
                if piece and self._check_valid(row, col, piece):
                    yield piece, row, col

    def get_tiles_and_coords(self):
        for i, row in enumerate(self._tiles):
            for j, tile in enumerate(row):
                yield tile, i, j

    def _generate_pieces(self) -> list[Piece]:
        pieces = []
        for _ in range(3):
            piece = random.choice(self._piece_vectors)
            pieces.append(Piece(piece["pos"], piece["color"]))
        return pieces

    def _check_valid(self, row: int, col: int, piece: Piece) -> bool:
        for tile_col, tile_row in piece.squares_pos:
            if not (
                0 <= row + tile_row < self.board_size
                and 0 <= col + tile_col < self.board_size
                and self._tiles[row + tile_row][col + tile_col].empty
            ):
                return False

        return True

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

    def _get_row(self, row: int) -> list[Tile]:
        return self._tiles[row]

    def _get_col(self, col: int) -> list[Tile]:
        return [row[col] for row in self._tiles]
