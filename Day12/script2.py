import bisect
from typing import Any
from dataclasses import dataclass
from collections import namedtuple
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
    
    #print(dijkstra(map, S, E))
    a_points = [a_point for a_point in map.elevations if map.elevations[a_point] == 0]
    distances_from_a_points = [dijkstra(map, a_point, E) for a_point in a_points]
    print(min(distances_from_a_points))

def dijkstra(map: Map, S: Point, E: Point):
    unvisited = list(map.elevations.keys())
    unvisited_set = set(unvisited)
    tentative_distances = dict()

    for node in map.elevations.keys():
        tentative_distances[node] = float("inf")
    tentative_distances[S] = 0
    unvisited.remove(S)
    unvisited.insert(0, S)

    current = S
    while unvisited:
        for neighbor in possible_moves(map, current):
            if neighbor in unvisited:
                new_distance = tentative_distances[current] + 1
                current_distance = tentative_distances[neighbor]
                if new_distance < current_distance:
                    tentative_distances[neighbor] = new_distance
                    unvisited.remove(neighbor)
                    bisect.insort(unvisited, neighbor, key=lambda node: tentative_distances[node])
        unvisited.remove(current)
        unvisited_set.remove(current)
        if E not in unvisited_set:
            return tentative_distances[E]
        
        current = find_next(unvisited)
        if current is None or tentative_distances[current] == float("inf"):
            return float("inf")
    
    raise Exception("?")

def find_next(unvisited):
    if unvisited:
        return unvisited[0]
    return None

def possible_moves(map: Map, cur: Point) -> list[Point]:
    up = Point(cur.x, cur.y - 1)
    down = Point(cur.x, cur.y + 1)
    left = Point(cur.x - 1, cur.y)
    right = Point(cur.x + 1, cur.y)
    return [target for target in [up, down, left, right] if possible_move(map, cur, target)]

def possible_move(map: Map, cur: Point, target: Point):
    if target.x > map.max.x or target.x < map.min.x \
        or target.y > map.max.y or target.y < map.min.y:
        return False
    
    return map.elevations[target] <= map.elevations[cur] + 1

if __name__ == "__main__":
    #import cProfile
    #cProfile.run("main()")
    main()
