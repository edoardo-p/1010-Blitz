import pygame
from constants import RADIUS, SPACING, TILE_SIZE


class Piece:
    def __init__(self, tiles: list[tuple[int, int]], color: pygame.Color):
        self.tiles = tiles
        self.color = color
        self.x = 0
        self.y = 0

    def update(self, x: int, y: int):
        self.x = x
        self.y = y

    def show(self, scale: float, screen: pygame.surface.Surface):
        for tile in self.tiles:
            pygame.draw.rect(
                screen,
                self.color,
                pygame.Rect(
                    tile[0] * scale * (TILE_SIZE + SPACING) + self.x,
                    tile[1] * scale * (TILE_SIZE + SPACING) + self.y,
                    TILE_SIZE * scale,
                    TILE_SIZE * scale,
                ),
                border_radius=RADIUS,
            )
