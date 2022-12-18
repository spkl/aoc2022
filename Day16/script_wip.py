import re
from dataclasses import dataclass, field
from collections import deque


@dataclass
class Valve:
    name: str
    flow_rate: int
    neighbor_names: list[str]
    neighbors: list['Valve'] = field(default_factory=list)
    open: bool = field(default=False)

    def resolve_neighbors(self, valves: list['Valve']):
        for neighbor_name in self.neighbor_names:
            self.neighbors.append(next(v for v in valves if v.name == neighbor_name))

def main():
    with open("example_input.txt", "r") as f:
        lines = [line.rstrip() for line in f.readlines()]
    valves = list(map(to_valve, (re.findall("Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z,\s]+)", line) for line in lines)))
    for valve in valves:
        valve.resolve_neighbors(valves)
    
    valve = next(v for v in valves if v.name == "AA")
    cur_time: int = 1
    max_time: int = 30
    pressure_released: int = 0
    way_time: int = 0
    while cur_time <= max_time:
        pressure_released += sum(v.flow_rate for v in valves if v.open)

        if way_time > 0:
            way_time -= 1
        elif valve.flow_rate > 0 and not valve.open:
            valve.open = True
        else:
            way_time, next_valve = get_best_unopened(valve, valves, max_time - cur_time)
            print(f"Moving to {next_valve.name if next_valve else '-'} in {way_time} steps")
            way_time -= 1
            if next_valve:
                valve = next_valve

        cur_time += 1
    
    print(pressure_released)

def to_valve(results: list[list[str]]) -> Valve:
    result = results[0]
    name = result[0]
    flow_rate = int(result[1])
    neighbor_names = result[2].split(", ")
    return Valve(name, flow_rate, neighbor_names)

def get_best_unopened(valve: Valve, valves: list[Valve], remaining_time: int) -> tuple[int, Valve]:
    match valve.name:
        case "AA":
            end = next(v for v in valves if v.name == "DD")
        case "DD":
            end = next(v for v in valves if v.name == "BB")
        case "BB":
            end = next(v for v in valves if v.name == "JJ")
        case "JJ":
            end = next(v for v in valves if v.name == "HH")
        case "HH":
            end = next(v for v in valves if v.name == "EE")
        case "EE":
            end = next(v for v in valves if v.name == "CC")
        case _:
            return (-1, None)
    
    return (len(bfs(valve, end)), end)

def bfs(start: Valve, end: Valve) -> list[Valve]:
    q: deque[list[Valve]] = deque()
    q.append([start])

    explored: set[str] = set([start.name])
    
    distances: dict[str, int] = dict()
    distances[start.name] = 0
    
    while q:
        path = q.popleft()
        current = path[-1]
        if current == end:
            return path[1::]
        for neighbor in current.neighbors:
            if neighbor.name not in explored:
                new_path = list(path)
                new_path.append(neighbor)
                explored.add(neighbor.name)
                q.append(new_path)
    
    return float("inf")

if __name__ == "__main__":
    # import cProfile
    # cProfile.run("main()")
    main()
