import pygame
from constants import BOARD_SIZE, GRID_X, GRID_Y, RADIUS, SPACING, TILE_SIZE
from piece import Piece
from tile import Tile


class Grid:
    def __init__(self):
        self._tiles = [Tile() for _ in range(BOARD_SIZE * BOARD_SIZE)]

    def show(self, header: str, screen: pygame.surface.Surface) -> None:
        font = pygame.font.Font(None, 50)
        text_surface = font.render(header, True, pygame.Color(0, 100, 200))
        screen.blit(text_surface, (20, 20))

        for idx, tile in enumerate(self._tiles):
            y, x = divmod(idx, BOARD_SIZE)
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
        if self._check_valid(row * BOARD_SIZE + col, piece):
            for tile_col, tile_row in piece.tiles:
                idx = (row + tile_row) * BOARD_SIZE + col + tile_col
                self._tiles[idx].update(piece.color)
            return self._clear_lines() + len(piece.tiles)

        return 0

    def has_lost(self, pieces: list[Piece]) -> bool:
        for idx, tile in enumerate(self._tiles):
            if not tile.empty:
                continue

            for piece in pieces:
                if self._check_valid(idx, piece):
                    return False

        return True

    def _check_valid(self, idx: int, piece: Piece) -> bool:
        for tile_col, tile_row in piece.tiles:
            curr_idx = idx + tile_row * BOARD_SIZE + tile_col
            if not (
                0 <= curr_idx < BOARD_SIZE * BOARD_SIZE
                # TODO implement check to avoid wraparound
                # and idx // BOARD_SIZE == curr_idx // BOARD_SIZE
                and self._tiles[curr_idx].empty
            ):
                return False

        return True

    def _clear_lines(self) -> int:
        lines = 0

        for row_num in range(BOARD_SIZE):
            row = self._get_row(row_num)
            if not any(tile.empty for tile in row):
                lines += 1
                for tile in row:
                    tile.update(pygame.Color(40, 40, 40))

        for col_num in range(BOARD_SIZE):
            col = self._get_col(col_num)
            if not any(tile.empty for tile in self._get_col(col_num)):
                lines += 1
                for tile in col:
                    tile.update(pygame.Color(40, 40, 40))

        return 5 * lines * (lines + 1)

    def _get_row(self, row: int) -> list[Tile]:
        return self._tiles[row * BOARD_SIZE : (row + 1) * BOARD_SIZE]

    def _get_col(self, col: int) -> list[Tile]:
        return self._tiles[col::BOARD_SIZE]
