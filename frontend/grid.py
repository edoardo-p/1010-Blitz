import pygame
from constants import BOARD_SIZE, GRID_X, GRID_Y, RADIUS, SPACING, TILE_SIZE
from piece import Piece
from tile import Tile


class Grid:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.tiles = [[Tile() for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def show(self, header: str, screen: pygame.surface.Surface):
        font = pygame.font.Font(None, 50)
        text_surface = font.render(header, True, pygame.Color(0, 100, 200))
        screen.blit(text_surface, (20, 20))

        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                pygame.draw.rect(
                    screen,
                    tile.color,
                    pygame.Rect(
                        GRID_X + x * (TILE_SIZE + SPACING),
                        GRID_Y + y * (TILE_SIZE + SPACING),
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

    def has_lost(self, pieces: list[Piece]) -> bool:
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if not self.tiles[row][col].empty:
                    continue

                for piece in pieces:
                    if self._check_valid(row, col, piece):
                        return False

        return True

    def _check_valid(self, row: int, col: int, piece: Piece) -> bool:
        for tile_col, tile_row in piece.tiles:
            curr_row = row + tile_row
            curr_col = col + tile_col
            if not (
                0 <= curr_row < BOARD_SIZE
                and 0 <= curr_col < BOARD_SIZE
                and self.tiles[curr_row][curr_col].empty
            ):
                return False

        return True

    def _check_lines(self) -> int:
        full_rows = []
        full_cols = []
        for row in range(BOARD_SIZE):
            if not any(tile.empty for tile in self.tiles[row]):
                full_rows.append(row)

        for col in range(BOARD_SIZE):
            if not any(self.tiles[row][col].empty for row in range(BOARD_SIZE)):
                full_cols.append(col)

        return self._clear_lines(full_rows, full_cols)

    def _clear_lines(self, full_rows: list[int], full_cols: list[int]) -> int:
        for row in full_rows:
            for i in range(BOARD_SIZE):
                self.tiles[row][i].update(pygame.Color(40, 40, 40))

        for col in full_cols:
            for i in range(BOARD_SIZE):
                self.tiles[i][col].update(pygame.Color(40, 40, 40))

        lines = len(full_rows) + len(full_cols)
        return 5 * lines * (lines + 1)
