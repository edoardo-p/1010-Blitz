from pygame import Color
from dataclasses import dataclass, field


@dataclass
class Tile:
    color: Color = field(default_factory=lambda: Color(0))
    empty: bool = True

    def update(self, color: Color):
        self.color = color
        self.empty = color == Color(0)
