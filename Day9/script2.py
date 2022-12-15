from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])

def main():
    with open("input.txt") as f:
        moves = [line.rstrip() for line in f.readlines()]
    
    head = Point(0, 0)
    tails = [Point(0, 0) for _ in range(9)]
    visited_points = set([tails[-1]])

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
            
            leader = head
            for i, follower in enumerate(tails):
                tails[i] = move_follower(follower, leader)
                leader = tails[i]
            
            visited_points.add(tails[-1])
    
    print(len(visited_points))

def move_follower(follower, leader):
    x_diff = leader.x - follower.x
    y_diff = leader.y - follower.y
    if (abs(x_diff) > 1 and abs(y_diff) > 0) or (abs(y_diff) > 1 and abs(x_diff) > 0):
        x_diff = cap_diff(x_diff)
        y_diff = cap_diff(y_diff)
        follower = Point(follower.x + x_diff, follower.y + y_diff)
    elif abs(x_diff) > 1:
        x_diff = cap_diff(x_diff)
        follower = Point(follower.x + x_diff, follower.y)
    elif abs(y_diff) > 1:
        y_diff = cap_diff(y_diff)
        follower = Point(follower.x, follower.y + y_diff)
    return follower

def cap_diff(diff):
    if diff > 1:
        return 1
    elif diff < -1:
        return -1
    return diff

if __name__ == "__main__":
    main()