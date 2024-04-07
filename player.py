
from enum import Enum
from position import Position


class PlayerType(Enum):
    RED = 1
    BLACK = 2


class Player:
    def __init__(self, color: PlayerType,
                 position: Position,
                 name: str = "") -> None:

        self.color = color
        self.position: Position = position
        self.name = name or color.name

    def __str__(self) -> str:
        return f"{self.name} is at {self.position}"
