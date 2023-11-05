from dataclasses import dataclass


@dataclass
class Tile:
    color: tuple[int, int, int] = (40, 40, 40)
    empty: bool = True

    def update(self, color: tuple[int, int, int]):
        self.color = color
        self.empty = False

    def clear(self):
        self.update((40, 40, 40))
        self.empty = True
