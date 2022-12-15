from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])

def main():
    with open("input.txt") as f:
        moves = [line.rstrip() for line in f.readlines()]
    
    head = Point(0, 0)
    tail = Point(0, 0)
    visited_points = set([tail])

    for move in moves:
        direction, amount = move.split(" ")
        amount = int(amount)
        for _ in range(amount):
            if direction == "L":
                head = Point(head.x - 1, head.y)
            elif direction == "R":
                head = Point(head.x + 1, head.y)
            elif direction == "U":
                head = Point(head.x, head.y - 1)
            elif direction == "D":
                head = Point(head.x, head.y + 1)
            else:
                raise Exception(f"Unknown direction {direction}")
            
            tail = move_tail(tail, head)
            visited_points.add(tail)
    
    print(len(visited_points))

def move_tail(tail, head):
    x_diff = head.x - tail.x
    y_diff = head.y - tail.y
    if (abs(x_diff) > 1 and abs(y_diff) > 0) or (abs(y_diff) > 1 and abs(x_diff) > 0):
        x_diff = cap_diff(x_diff)
        y_diff = cap_diff(y_diff)
        tail = Point(tail.x + x_diff, tail.y + y_diff)
    elif abs(x_diff) > 1:
        x_diff = cap_diff(x_diff)
        tail = Point(tail.x + x_diff, tail.y)
    elif abs(y_diff) > 1:
        y_diff = cap_diff(y_diff)
        tail = Point(tail.x, tail.y + y_diff)
    return tail

def cap_diff(diff):
    if diff > 1:
        return 1
    elif diff < -1:
        return -1
    return diff

if __name__ == "__main__":
    main()