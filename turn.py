from enum import Enum
from turtle import st
from position import Position


class TurnType(Enum):
    MOVE = 1
    SWAP = 2


class Turn:
    def __init__(self, type: TurnType, start: Position, end: Position) -> None:
        self.type: TurnType = type
        self.start: Position = start
        self.end: Position = end
