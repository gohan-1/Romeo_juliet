
from enum import Enum
from position import Position


class PlayerType(Enum):
    RED = 1
    BLACK = 2


class Player:
    def __init__(self, color: PlayerType,
                 position: Position = Position(0, 0),
                 name: str = "Player") -> None:

        self.color = color
        self.position: Position = position
        self.name = name
        
