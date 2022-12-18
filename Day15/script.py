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


class Verdict(Enum):
    UNKNOWN = auto()
    SENSOR = auto()
    BEACON = auto()
    NO_BEACON = auto()

def main():
    with open("input.txt", "r") as f:
        lines = [line.rstrip() for line in f.readlines()]
    
    sensor_infos = list(map(to_sensor_info, (re.findall("\-?\d+", line) for line in lines)))
    grid = defaultdict(lambda: Verdict.UNKNOWN)
    
    row = 2000000
    # row = 10

    for sensor_info in sensor_infos:
        grid[sensor_info.b_pos] = Verdict.BEACON
        grid[sensor_info.s_pos] = Verdict.SENSOR
        
        min_x = sensor_info.s_pos[X] - sensor_info.distance
        max_x = sensor_info.s_pos[X] + sensor_info.distance + 1
        min_y = sensor_info.s_pos[Y] - sensor_info.distance
        max_y = sensor_info.s_pos[Y] + sensor_info.distance + 1

        print(f"{sensor_infos.index(sensor_info) + 1}/{len(sensor_infos)} - {max_x - min_x},{max_y - min_y}")

        if min_y > row or max_y < row:
            continue
        
        for x in range(min_x, max_x):
            pos = (x, row)
            if dist(pos, sensor_info.s_pos) <= sensor_info.distance:
                if grid[pos] == Verdict.UNKNOWN:
                    grid[pos] = Verdict.NO_BEACON
    
    # print_grid(grid)
    
    grid_min = min_pos(grid)
    grid_max = max_pos(grid)

    no_beacon_count = 0
    for x in range(grid_min[X], grid_max[X] + 1):
        pos = (x, row)
        verdict = grid[pos]
        if verdict == Verdict.NO_BEACON:
            no_beacon_count += 1
    print(no_beacon_count)

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
                    raise Exception(f"Unknown verdict {other}")
            print(char, end="")
        print()

if __name__ == "__main__":
    # import cProfile
    # cProfile.run("main()")
    main()
