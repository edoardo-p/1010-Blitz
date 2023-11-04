import pygame
from constants import BOARD_SIZE, GRID_X, GRID_Y, RADIUS, SPACING, TILE_SIZE


class Board:
    def show(self, score: int, screen: pygame.surface.Surface):
        font = pygame.font.Font(None, 50)
        text_surface = font.render(str(score), True, pygame.Color(0, 100, 200))
        screen.blit(text_surface, (20, 20))

        for i in range(BOARD_SIZE * BOARD_SIZE):
            x, y = divmod(i, BOARD_SIZE)
            pygame.draw.rect(
                screen,
                pygame.Color(40, 40, 40),
                pygame.Rect(
                    GRID_X + x * (TILE_SIZE + SPACING),
                    GRID_Y + y * (TILE_SIZE + SPACING),
                    TILE_SIZE,
                    TILE_SIZE,
                ),
                border_radius=RADIUS,
            )
