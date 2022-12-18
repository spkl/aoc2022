import re
from dataclasses import dataclass
from enum import Enum, auto
from collections import defaultdict
from typing import Iterator
from itertools import chain

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
    
    def rim(self) -> Iterator[tuple[int, int]]:
        return chain(
            self.rim_tr(),
            self.rim_tl(),
            self.rim_br(),
            self.rim_bl())
    
    def rim_tr(self) -> Iterator[tuple[int, int]]:
        dist = self.distance
        for delta in range(0, dist):
            yield (self.s_pos[X] + delta, self.s_pos[Y] - dist + delta)
    
    def rim_tl(self) -> Iterator[tuple[int, int]]:
        dist = self.distance
        for delta in range(1, dist + 1):
            yield (self.s_pos[X] - delta, self.s_pos[Y] - dist + delta)
    
    def rim_br(self) -> Iterator[tuple[int, int]]:
        dist = self.distance
        for delta in range(1, dist + 1):
            yield (self.s_pos[X] + delta, self.s_pos[Y] + dist - delta)
    
    def rim_bl(self) -> Iterator[tuple[int, int]]:
        dist = self.distance
        for delta in range(0, dist):
            yield (self.s_pos[X] - delta, self.s_pos[Y] + dist - delta)


class Verdict(Enum):
    UNKNOWN = auto()
    SENSOR = auto()
    BEACON = auto()
    NO_BEACON = auto()

def main():
    with open("input.txt", "r") as f:
        lines = [line.rstrip() for line in f.readlines()]
    
    sensor_infos = list(map(to_sensor_info, (re.findall("\-?\d+", line) for line in lines)))
    
    # global_min = 0
    # global_max = 20
    global_min = 0
    global_max = 4000000

    in_global_bounds = lambda pos: pos[X] <= global_max and pos[Y] <= global_max and pos[X] >= global_min and pos[Y] >= global_min
    print("Getting top right rims...")
    points_tr = set(filter(in_global_bounds, chain(*(sensor_info.rim_tr() for sensor_info in sensor_infos))))
    print("Getting top left rims...")
    points_tl = set(filter(in_global_bounds, chain(*(sensor_info.rim_tl() for sensor_info in sensor_infos))))
    print("Getting bottom right rims...")
    points_br = set(filter(in_global_bounds, chain(*(sensor_info.rim_br() for sensor_info in sensor_infos))))
    print("Getting bottom left rims...")
    points_bl = set(filter(in_global_bounds, chain(*(sensor_info.rim_bl() for sensor_info in sensor_infos))))
    
    print("Intersecting top...")
    isect_t = points_tr.intersection(points_tl)
    print("Intersecting bottom...")
    isect_b = points_br.intersection(points_bl)
    print("Intersecting right...")
    isect_r = points_tr.intersection(points_br)
    print("Intersecting left...")
    isect_l = points_bl.intersection(points_tl)

    # print(isect_t) #14,12
    # print(isect_b) #14,10
    # print(isect_r) #13,11
    # print(isect_l) #15,11

    for t_pos in isect_t:
        b_pos = (t_pos[X], t_pos[Y] - 2)
        r_pos = (t_pos[X] - 1, t_pos[Y] - 1)
        l_pos = (t_pos[X] + 1, t_pos[Y] - 1)
        if b_pos in isect_b and r_pos in isect_r and l_pos in isect_l:
            c_pos = (t_pos[X], t_pos[Y] - 1)
            print(c_pos, c_pos[X] * 4000000 + c_pos[Y])


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
