from collections import defaultdict
from dataclasses import dataclass, field

@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int

@dataclass
class MovablePoint:
    x: int
    y: int

@dataclass
class Rock:
    points: list[Point]

@dataclass
class Cave:
    grid: dict[Point, str] = field(default_factory=lambda: defaultdict(lambda: "."))
    min: Point = None
    max: Point = None

    def calc_extent(self):
        self.min = Point(min(point.x for point in self.grid), min(point.y for point in self.grid))
        self.max = Point(max(point.x for point in self.grid), max(point.y for point in self.grid))
    
    def contains(self, point: Point) -> bool:
        return point.x >= self.min.x and point.x <= self.max.x \
            and point.y >= self.min.y and point.y <= self.max.y

def main():
    with open("input.txt", "r") as f:
        rock_strings = [line.rstrip() for line in f.readlines()]
    
    rocks = get_rocks(rock_strings)

    sand_source = Point(500, 0)
    cave = Cave()
    cave.grid[sand_source] = "+"
    add_rocks(cave, rocks)
    cave.calc_extent()
    
    grains = 0
    while place_grain(cave, sand_source):
        grains += 1

    print(grains)

def place_grain(cave: Cave, sand_source: Point) -> bool:
    p = MovablePoint(sand_source.x, sand_source.y)
    while move_d(cave, p) or move_dl(cave, p) or move_dr(cave, p):
        if not cave.contains(Point(p.x, p.y)):
            return False
    
    final_point = Point(p.x, p.y)    
    cave.grid[final_point] = "o"
    return True

def move_d(cave: Cave, p: MovablePoint) -> bool:
    return move(cave, p, (0, 1))

def move_dl(cave: Cave, p: MovablePoint) -> bool:
    return move(cave, p, (-1, 1))

def move_dr(cave: Cave, p: MovablePoint) -> bool:
    return move(cave, p, (1, 1))

def move(cave: Cave, p: MovablePoint, vector: tuple[int, int]) -> bool:
    new_point = Point(p.x + vector[0], p.y + vector[1])
    if cave.grid[new_point] == ".":
        p.x = new_point.x
        p.y = new_point.y
        return True
    return False

def add_rocks(cave: Cave, rocks: list[Rock]):
    for rock in rocks:
        draw_rock(cave, rock)

def draw_rock(cave: Cave, rock: Rock):
    for i in range(len(rock.points) - 1):
        start = rock.points[i]
        stop = rock.points[i + 1]
        for x in from_to(start.x, stop.x):
            for y in from_to(start.y, stop.y):
                cave.grid[Point(x, y)] = "#"

def from_to(start: int, stop: int):
    if start <= stop:
        return range(start, stop + 1, 1)
    return range(start, stop - 1, -1)

def get_rocks(rock_strings: list[str]) -> list[Rock]:
    rocks = []
    for rock_string in rock_strings:
        points = []
        for point_string in rock_string.split(" -> "):
            x, y = point_string.split(",")
            points.append(Point(int(x), int(y)))
        rocks.append(Rock(points))
    return rocks

if __name__ == "__main__":
    main()
