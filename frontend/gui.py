import pygame
from constants import BOARD_SIZE, GRID_X, GRID_Y, RADIUS, SPACING, TILE_SIZE
from game import Game
from piece import Piece


def show_game(
    screen: pygame.surface.Surface, game: Game, header: str | None = None
) -> None:
    font = pygame.font.Font(None, 50)
    text = str(game.score) if header == None else header
    text_surface = font.render(text, True, pygame.Color(0, 100, 200))
    screen.blit(text_surface, (20, 20))

    for idx, tile in enumerate(game.tiles):
        y, x = divmod(idx, BOARD_SIZE)
        pygame.draw.rect(
            screen,
            pygame.Color(*tile.color),
            pygame.Rect(
                GRID_X + x * (TILE_SIZE + SPACING),
                GRID_Y + y * (TILE_SIZE + SPACING),
                TILE_SIZE,
                TILE_SIZE,
            ),
            border_radius=RADIUS,
        )


def show_piece(
    screen: pygame.surface.Surface, piece: Piece, scale: float = 1.0
) -> None:
    for tile in piece.tiles:
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
