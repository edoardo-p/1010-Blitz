from dataclasses import dataclass


@dataclass
class Piece:
    squares_pos: list[tuple[int, int]]
    color: tuple[int, int, int]

    def __post_init__(self):
        self.update(0, 0)

    def update(self, x: int, y: int):
        self.x = x
        self.y = y
