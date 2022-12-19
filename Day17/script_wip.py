import re
from dataclasses import dataclass, field
from collections import deque

@dataclass
class Line:
    positions: tuple[int]

    @property
    def is_empty(self):
        return not any(pos != 0 for pos in self.positions)

    def get_empty():
        return Line((0, 0, 0, 0, 0, 0, 0))

@dataclass
class Shape:
    lines: list[Line]

@dataclass
class MovingShape:
    shape: Shape
    pos: int

class Jets:
    def __init__(self, input: str):
        self.directions = [(-1 if char == '<' else 1) for char in input]
    
    def __iter__(self):
        while True:
            for direction in self.directions:
                yield direction

class Shapes:
    def __init__(self):
        self.list = [
            Shape([Line((1, 1, 1, 1))]), # HLine
            Shape([Line((0, 1, 0)), Line((1, 1, 1)), Line((0, 1, 0))]), # Plus
            Shape([Line((0, 0, 1)), Line((0, 0, 1)), Line((1, 1, 1))]), # Corner
            Shape([Line((1,)), Line((1,)), Line((1,)), Line((1,))]), # VLine
            Shape([Line((1, 1)), Line((1, 1))]) # Block
        ]
    
    def __iter__(self):
        while True:
            for shape in self.list:
                yield shape

@dataclass
class Chamber:
    lines: list[Line] = field(default_factory=lambda: [Line.get_empty(), Line.get_empty(), Line.get_empty()])

    def ensure_empty_lines(self, height: int):
        while len(self.lines) < height or any(not line.is_empty for line in self.lines[-height:]):
            self.lines.append(Line.get_empty())

def main():
    with open("example_input.txt", "r") as f:
        lines = [line.rstrip() for line in f.readlines()]
    
    jets: Jets = Jets(lines[0])
    shapes: Shapes = Shapes()
    chamber: Chamber = Chamber()




if __name__ == "__main__":
    main()
