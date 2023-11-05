from dataclasses import dataclass, field

from pygame import Color


@dataclass
class Tile:
    color: Color = field(default_factory=lambda: Color(40, 40, 40))
    empty: bool = True

    def update(self, color: Color):
        self.color = color
        self.empty = False

    def clear(self):
        self.update(Color(40, 40, 40))
        self.empty = True
