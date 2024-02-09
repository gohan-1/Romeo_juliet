class Position:
    def __init__(self, _x, _y) -> None:
        self.x = _x
        self.y = _y

    def __str__(self) -> str:
        return f"({self.x+1}, {self.y+1})"

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Position):
            raise NotImplemented
        return __value.x == self.x and __value.y == self.y
