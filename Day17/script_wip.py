import re
from dataclasses import dataclass, field
from enum import Enum, auto
from collections import deque

V_START_POS = 3
H_START_POS = 2
C_WIDTH = 7

class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()

@dataclass
class Line:
    positions: tuple[int]

    @property
    def is_empty(self) -> bool:
        return not any(pos != 0 for pos in self.positions)

    @property
    def width(self) -> int:
        return len(self.positions)

    def get_empty() -> 'Line':
        return Line(tuple(0 for _ in range(C_WIDTH)))

@dataclass
class Shape:
    lines: list[Line]

    @property
    def width(self) -> int:
        return self.lines[0].width
    
    @property
    def height(self) -> int:
        return len(self.lines)

@dataclass
class MovingShape:
    shape: Shape
    h_pos: int
    """The horizontal position of the leftmost part of the shape."""
    v_pos: int
    """The vertical position of the uppermost part of the shape."""

    def can_move(self, d: Direction, c: 'Chamber') -> bool:
        new_h_pos = self._get_new_h_pos(d)
        if new_h_pos < 0 or new_h_pos + self.shape.width > C_WIDTH:
            return False
        
        projections = self._get_projections(c, new_h_pos, self.v_pos)
        for projection in projections:
            if 2 in projection:
                return False
        return True
    
    def move(self, d: Direction):
        self.h_pos = self._get_new_h_pos(d)
    
    def can_fall(self, c: 'Chamber') -> bool:
        new_v_pos = self.v_pos - 1
        if new_v_pos < 0:
            return False
        projections = self._get_projections(c, self.h_pos, new_v_pos)
        for projection in projections:
            if 2 in projection:
                return False
        return True

    def fall(self):
        self.v_pos = self.v_pos - 1
    
    def freeze(self, c: 'Chamber'):
        projections = self._get_projections(c, self.h_pos, self.v_pos)
        for v in reversed(range(self.shape.height)):
            c.lines[self.v_pos - v].positions = tuple(projections[v])

    def _get_new_h_pos(self, d):
        if d == Direction.LEFT:
            start = self.h_pos - 1
        elif d == Direction.RIGHT:
            start = self.h_pos + 1
        return start

    def _get_projections(self, c: 'Chamber', new_h_pos: int, new_v_pos: int) -> list[int]:
        projections = []
        for line in self.shape.lines:
            projection = []
            for _ in range(new_h_pos):
                projection.append(0)
            for pos in line.positions:
                projection.append(pos)
            while len(projection) < C_WIDTH:
                projection.append(0)
            projections.append(projection)
        
        for v in reversed(range(self.shape.height)):
            projections[v] = [sum(z) for z in zip(projections[v], c.lines[new_v_pos - v].positions)]
        return projections


class Jets:
    def __init__(self, input: str):
        self.directions = [(Direction.LEFT if char == '<' else Direction.RIGHT) for char in input]
    
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

    @property
    def height(self) -> int:
        return len(self.lines)

    @property
    def width(self) -> int:
        return self.lines[0].width

def main():
    with open("example_input.txt", "r") as f:
        lines = [line.rstrip() for line in f.readlines()]
    
    jets = iter(Jets(lines[0]))
    shapes = iter(Shapes())
    chamber: Chamber = Chamber()

    for _ in range(2022):
        template = next(shapes)
        chamber.ensure_empty_lines(template.height + V_START_POS)
        shape = MovingShape(template, H_START_POS, chamber.height - 1)
        while True:
            direction = next(jets)
            if shape.can_move(direction, chamber):
                shape.move(direction)
            if shape.can_fall(chamber):
                shape.fall()
            else:
                shape.freeze(chamber)
                break
    
    print(sum(1 for line in chamber.lines if not line.is_empty))


if __name__ == "__main__":
    main()
