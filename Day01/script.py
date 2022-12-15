def main():
    with open("input.txt") as f:
        calories = 0
        elves = []
        for line in f:
            line = line.rstrip()
            if line == '':
                elves.append(calories)
                calories = 0
            else:
                calories = calories + int(line)
    
    elves = sorted(elves, reverse=True)
    top_elves = elves[:3]
    print(top_elves)
    print(sum(top_elves))

if __name__ == "__main__":
    main()