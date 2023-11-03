import pygame
from constants import BOARD_SIZE, RADIUS, SPACING, TILE_SIZE


class Board:
    def __init__(self):
        self.x = 20
        self.y = 60
        self.height = 250

        self.bgd_colour = pygame.Color(40, 40, 40)
        self.text_colour = pygame.Color(0, 100, 200)

    def show(self, score: int, screen: pygame.surface.Surface):
        font = pygame.font.Font(None, 50)
        text_surface = font.render(str(score), True, self.text_colour)
        screen.blit(text_surface, (20, 20))

        for i in range(BOARD_SIZE * BOARD_SIZE):
            x, y = divmod(i, BOARD_SIZE)
            pygame.draw.rect(
                screen,
                self.bgd_colour,
                pygame.Rect(
                    self.x + x * (TILE_SIZE + SPACING),
                    self.y + y * (TILE_SIZE + SPACING),
                    TILE_SIZE,
                    TILE_SIZE,
                ),
                border_radius=RADIUS,
            )
