import pygame
from constants import BOARD_SIZE, RADIUS, SPACING, TILE_SIZE
from piece import Piece
from tile import Tile


class Grid:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.tiles = [[Tile() for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def show(self, screen: pygame.surface.Surface):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if not tile.empty:
                    pygame.draw.rect(
                        screen,
                        tile.color,
                        pygame.Rect(
                            self.x + x * (TILE_SIZE + SPACING),
                            self.y + y * (TILE_SIZE + SPACING),
                            TILE_SIZE,
                            TILE_SIZE,
                        ),
                        border_radius=RADIUS,
                    )

    def update(self, row: int, col: int, piece: Piece) -> int:
        if self._check_valid(row, col, piece):
            for tile_col, tile_row in piece.tiles:
                self.tiles[row + tile_row][col + tile_col].update(piece.color)
            return self._check_lines() + len(piece.tiles)

        return 0

    def _check_valid(self, row: int, col: int, piece: Piece) -> bool:
        for tile_col, tile_row in piece.tiles:
            curr_row = row + tile_row
            curr_col = col + tile_col
            if not (
                0 <= curr_row < len(self.tiles)
                and 0 <= curr_col < len(self.tiles)
                and self.tiles[curr_row][curr_col].empty
            ):
                return False

        return True

    def _check_lines(self) -> int:
        full_rows = []
        full_cols = []
        for row in range(len(self.tiles)):
            for col in range(len(self.tiles)):
                if self.tiles[row][col].empty:
                    break

                if col == 9:
                    full_rows.append(row)

        for col in range(len(self.tiles)):
            for row in range(len(self.tiles)):
                if self.tiles[row][col].empty:
                    break

                if row == 9:
                    full_cols.append(col)

        return self._clear_lines(full_rows, full_cols)

    def _clear_lines(self, full_rows: list[int], full_cols: list[int]) -> int:
        for row in full_rows:
            for i in range(BOARD_SIZE):
                self.tiles[row][i].update(pygame.Color(0))

        for col in full_cols:
            for i in range(BOARD_SIZE):
                self.tiles[col][i].update(pygame.Color(0))

        lines = len(full_rows) + len(full_cols)
        return 5 * lines * (lines + 1)

    def has_lost(self, pieces: list[Piece]) -> bool:
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if not self.tiles[row][col].empty:
                    continue

                for piece in pieces:
                    if self._check_valid(row, col, piece):
                        return False

        return True
