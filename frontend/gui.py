import pygame
from .parameters import (
    GRID_HEIGHT,
    GRID_X,
    GRID_Y,
    RADIUS,
    SPACING,
    TILE_SIZE,
    WIN_WIDTH,
)

from backend.game import Game
from backend.piece import Piece


def draw_game(
    screen: pygame.surface.Surface, game: Game, header: str | None = None
) -> None:
    font = pygame.font.Font(None, 50)
    text = str(game.score) if header == None else header
    text_surface = font.render(text, True, pygame.Color(0, 100, 200))
    screen.blit(text_surface, (20, 20))

    for tile, row, col in game.get_tiles_and_coords():
        pygame.draw.rect(
            screen,
            pygame.Color(*tile.color),
            pygame.Rect(
                GRID_X + col * (TILE_SIZE + SPACING),
                GRID_Y + row * (TILE_SIZE + SPACING),
                TILE_SIZE,
                TILE_SIZE,
            ),
            border_radius=RADIUS,
        )


def draw_piece(
    screen: pygame.surface.Surface, piece: Piece, scale: float = 1.0
) -> None:
    for tile in piece.squares_pos:
        pygame.draw.rect(
            screen,
            pygame.Color(*piece.color),
            pygame.Rect(
                tile[0] * scale * (TILE_SIZE + SPACING) + piece.x,
                tile[1] * scale * (TILE_SIZE + SPACING) + piece.y,
                TILE_SIZE * scale,
                TILE_SIZE * scale,
            ),
            border_radius=RADIUS,
        )


def draw_piece_menu(screen: pygame.surface.Surface, pieces: list[Piece]):
    for i, piece in enumerate(pieces):
        piece.update(WIN_WIDTH * i // 3 + TILE_SIZE * 2, GRID_HEIGHT + TILE_SIZE * 4)
        draw_piece(screen, piece, 0.5)
