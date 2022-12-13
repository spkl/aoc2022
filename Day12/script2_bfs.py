from dataclasses import dataclass
from collections import namedtuple
from queue import Queue
from collections import deque
Point = namedtuple("Point", ["x", "y"])

@dataclass
class Map:
    min: Point
    max: Point
    elevations: dict[Point, int]

def main():
    with open("input.txt", "r") as f:
        lines = [line.rstrip() for line in f.readlines()]
    
    S: Point = None
    E: Point = None

    elevations = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "S":
                S = Point(x, y)
                char = "a"
            elif char == "E":
                E = Point(x, y)
                char = "z"
            elevations[Point(x, y)] = ord(char) - ord("a")
    
    map = Map(min(elevations.keys()), max(elevations.keys()), elevations)
    
    #print(bfs(map, S, E))
    a_points = [a_point for a_point in map.elevations if map.elevations[a_point] == 0]
    distances_from_a_points = [bfs(map, a_point, E) for a_point in a_points]
    distances_from_a_points = [distance for distance in distances_from_a_points if distance != float("inf")]
    print(f"len={len(distances_from_a_points)}")
    print(min(distances_from_a_points))

def bfs(map: Map, S: Point, E: Point):
    q = deque()
    q.append(S)

    explored = set([S])
    
    distances = dict()
    distances[S] = 0
    
    while q:
        current = q.popleft()
        if current == E:
            return distances[current]
        for neighbor in possible_moves(map, current):
            if neighbor not in explored:
                distances[neighbor] = distances[current] + 1
                explored.add(neighbor)
                q.append(neighbor)
    
    return float("inf")


def possible_moves(map: Map, cur: Point) -> list[Point]:
    up = Point(cur.x, cur.y - 1)
    down = Point(cur.x, cur.y + 1)
    left = Point(cur.x - 1, cur.y)
    right = Point(cur.x + 1, cur.y)
    return (target for target in (up, down, left, right) if possible_move(map, cur, target))

def possible_move(map: Map, cur: Point, target: Point):
    if target.x > map.max.x or target.x < map.min.x \
        or target.y > map.max.y or target.y < map.min.y:
        return False
    
    return map.elevations[target] <= map.elevations[cur] + 1

if __name__ == "__main__":
    #import cProfile
    #cProfile.run("main()")
    from timeit import default_timer as timer
    start = timer()
    main()
    end = timer()
    print(end - start)
