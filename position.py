class Position:
    def __init__(self, _x, _y) -> None:
        self.x = _x
        self.y = _y

    def __str__(self) -> str:
        return f"({self.x+1}, {self.y+1})"
