from dataclasses import dataclass, field
from enum import Enum, auto

V_START_POS = 3
H_START_POS = 2
C_WIDTH = 7
PATTERN_SEARCH_COUNT = 5000

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

    def print(self):
        for pos in self.positions:
            char = "." if pos == 0 else "#"
            print(char, end="")
        print()

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
    _calculated_h_pos: int = field(default=-1)
    _shape_projections: list = field(default_factory=list)

    def can_move(self, d: Direction, c: 'Chamber', needs_projections: bool) -> bool:
        new_h_pos = self._get_new_h_pos(d)
        if new_h_pos < 0 or new_h_pos + self.shape.width > C_WIDTH:
            return False
        
        if not needs_projections:
            return True
        
        projections = self._get_projections(c, new_h_pos, self.v_pos)
        for projection in projections:
            if 2 in projection:
                return False
        return True
    
    def move(self, d: Direction):
        self.h_pos = self._get_new_h_pos(d)
    
    def can_fall(self, c: 'Chamber', needs_projections: bool) -> bool:
        new_v_pos = self.v_pos - 1
        if new_v_pos < 0:
            return False

        if not needs_projections:
            return True

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
        projections = list(self._get_shape_projections(new_h_pos))
        for v in range(self.shape.height):
            projections[v] = [a + b for a, b in zip(projections[v], c.lines[new_v_pos - v].positions)]
        return projections

    def _get_shape_projections(self, new_h_pos):
        if new_h_pos == self._calculated_h_pos:
            return self._shape_projections

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
        
        self._calculated_h_pos = new_h_pos
        self._shape_projections = projections
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
    def filled_height(self) -> int:
        height = len(self.lines)
        for line in reversed(self.lines):
            if not line.is_empty:
                return height
            height -= 1
        return 0

    @property
    def width(self) -> int:
        return self.lines[0].width
    
    def print(self):
        for line in reversed(self.lines):
            line.print()
        print()

def main():
    with open("input.txt", "r") as f:
        lines = [line.rstrip() for line in f.readlines()]
    
    jets = iter(Jets(lines[0]))
    shapes = iter(Shapes())
    chamber: Chamber = Chamber()

    heights = []
    for _ in range(PATTERN_SEARCH_COUNT):
        heights.append(chamber.filled_height)
        template = next(shapes)
        chamber.ensure_empty_lines(template.height + V_START_POS)
        shape = MovingShape(template, H_START_POS, chamber.filled_height + V_START_POS + template.height - 1)
        projectionless_moves = V_START_POS
        while True:
            needs_projections = projectionless_moves < 1
            projectionless_moves -= 1
            direction = next(jets)
            if shape.can_move(direction, chamber, needs_projections):
                shape.move(direction)
            if shape.can_fall(chamber, needs_projections):
                shape.fall()
            else:
                shape.freeze(chamber)
                break
        
        if _ % 1000 == 0:
            print(_)

    # calculate height difference between each of the calculated rounds
    diffs = []
    for i, cur_height in enumerate(heights):
        if i + 1 > len(heights) - 1:
            break
        next_height = heights[i + 1]
        diffs.append(next_height - cur_height)

    # find repeating pattern in the height differences
    start_pos, pattern = find_repeating_pattern(diffs)
    print(start_pos, len(pattern))

    # start with the height from the round where the pattern starts
    target_rounds = 1000000000000
    rounds_from_start_pos = target_rounds - start_pos
    height = heights[start_pos]
    
    # add the pattern height as many times as possible
    pattern_height = sum(pattern)
    pattern_cycles = rounds_from_start_pos // len(pattern)
    height += pattern_height * pattern_cycles
    
    # only a part of the pattern remains until the target round,
    # add height diffs one-by-one
    rest_values = iter(pattern)
    rest_cycles = rounds_from_start_pos % len(pattern)
    for _ in range(rest_cycles):
        height += next(rest_values)
    
    print(height)

def find_repeating_pattern(seq: list[int]):
    start_pos, pattern = -1, []
    for i in range(len(seq)):
        for j in range(len(seq) - 1, i, -1):
            length = j - i
            if seq[i:j] == seq[i + length:j + length] and validate_pattern(seq, i, seq[i:j]):
                start_pos, pattern =  i, seq[i:j]
                break
        if start_pos != -1:
            break
    
    while len(pattern) % 2 == 0 and pattern[:len(pattern)//2] == pattern[len(pattern)//2:]:
        pattern = pattern[:len(pattern)//2]
    
    return start_pos, pattern

def validate_pattern(seq, start_pos, pattern):
    seq = seq[start_pos:]
    i_pattern = 0
    for pos in seq:
        if pos != pattern[i_pattern]:
            return False
        i_pattern = (i_pattern + 1) % len(pattern)
    return True

if __name__ == "__main__":
    # import cProfile
    # cProfile.run("main()")
    main()
