import re
from dataclasses import dataclass
from enum import Enum, auto
from collections import defaultdict

X = 0
Y = 1

@dataclass
class SensorInfo:
    s_pos: tuple[int, int]
    b_pos: tuple[int, int]
    _dist: int = None

    @property
    def distance(self):
        if self._dist is None:
            self._dist = dist(self.s_pos, self.b_pos)
        return self._dist
    
    def sensor_rim(self):
        dist = self.distance
        for delta in range(0, self.distance + 1):
            yield (self.s_pos[X] + delta, self.s_pos[Y] - dist + delta)
            yield (self.s_pos[X] - delta, self.s_pos[Y] - dist + delta)
            yield (self.s_pos[X] + delta, self.s_pos[Y] + dist - delta)
            yield (self.s_pos[X] - delta, self.s_pos[Y] + dist - delta)


class Verdict(Enum):
    UNKNOWN = auto()
    SENSOR = auto()
    BEACON = auto()
    NO_BEACON = auto()

def main():
    with open("example_input.txt", "r") as f:
        lines = [line.rstrip() for line in f.readlines()]
    
    sensor_infos = list(map(to_sensor_info, (re.findall("\-?\d+", line) for line in lines)))
    grid = defaultdict(lambda: Verdict.UNKNOWN)
    
    global_min = 0
    global_max = 20
    # global_min = 0
    # global_max = 4000000

    rim_points = defaultdict(lambda: 0)

    for sensor_info in sensor_infos:
        grid[sensor_info.b_pos] = Verdict.BEACON
        grid[sensor_info.s_pos] = Verdict.SENSOR

        for pos in sensor_info.sensor_rim():
            if pos[X] > global_max or pos[Y] > global_max or pos[X] < global_min or pos[Y] < global_min:
                continue
            # if grid[pos] == Verdict.UNKNOWN:
            grid[pos] = Verdict.NO_BEACON
            rim_points[pos] = rim_points[pos] + 1
    # grid[(14,11)] = None
    print_grid(grid)
    # print([pos for pos in rim_points if rim_points[pos] > 1])
    for top in list(rim_points):
        bottom = (top[X], top[Y] + 2)
        left = (top[X] - 1, top[Y] - 1)
        right = (top[X] + 1, top[Y] - 1)
        if rim_points[top] > 0 and rim_points[bottom] > 0 and rim_points[left] > 0 and rim_points[right] > 0:
            center = (top[X], top[Y] - 1)
            # print(center)

def to_sensor_info(res):
    return SensorInfo(to_int_pair(res, 0), to_int_pair(res, 2))

def to_int_pair(strs, offset):
    return (int(strs[offset + 0]), int(strs[offset + 1]))

def dist(a, b):
    return abs(a[X] - b[X]) + abs(a[Y] - b[Y])

def min_pos(grid):
    return (min(pos[X] for pos in grid), min(pos[Y] for pos in grid))

def max_pos(grid):
    return (max(pos[X] for pos in grid), max(pos[Y] for pos in grid))

def print_grid(grid):
    grid_min = min_pos(grid)
    grid_max = max_pos(grid)
    for y in range(grid_min[Y], grid_max[Y] + 1):
        for x in range(grid_min[X], grid_max[X] + 1):
            pos = (x, y)
            match grid[pos]:
                case Verdict.UNKNOWN:
                    char = "."
                case Verdict.SENSOR:
                    char = "S"
                case Verdict.BEACON:
                    char = "B"
                case Verdict.NO_BEACON:
                    char = "#"
                case other:
                    char = "?"
            print(char, end="")
        print()

if __name__ == "__main__":
    # import cProfile
    # cProfile.run("main()")
    main()
