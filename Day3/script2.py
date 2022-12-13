def get_priority(item_type):
    if item_type.islower():
        return ord(item_type) - ord("a") + 1
    else:
        return ord(item_type) - ord("A") + 27

def main():
    group = list()
    sum = 0
    with open("input.txt", "r") as f:
        for line in f:
            rucksack = line.rstrip()
            group.append(rucksack)
            if len(group) == 3:
                common_item_types = set(group[0]).intersection(group[1]).intersection(group[2])
                common_item_type = next(iter(common_item_types))
                sum += get_priority(common_item_type)
                group.clear()
    print(sum)

if __name__ == "__main__":
    main()
