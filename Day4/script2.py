def get_ranges(line):
    left, right = line.split(",")
    return (get_range(left), get_range(right))

def get_range(assignments):
    start, end = assignments.split("-")
    start, end = int(start), int(end) + 1
    return range(start, end)

def main():
    overlap_pairs = 0
    with open("input.txt", "r") as f:
        for line in f:
            line = line.rstrip()
            left_range, right_range = get_ranges(line)
            left_set = set(left_range)
            right_set = set(right_range)
            if not left_set.isdisjoint(right_set):
                overlap_pairs += 1
    
    print(overlap_pairs)

if __name__ == "__main__":
    main()
