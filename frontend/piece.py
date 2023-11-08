class Piece:
    def __init__(self, squares_pos: list[tuple[int, int]], color: tuple[int, int, int]):
        self.tiles = squares_pos
        self.color = color
        self.x = 0
        self.y = 0

    def update(self, x: int, y: int):
        self.x = x
        self.y = y
