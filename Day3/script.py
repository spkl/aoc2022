def get_priority(item_type):
    if item_type.islower():
        return ord(item_type) - ord("a") + 1
    else:
        return ord(item_type) - ord("A") + 27

def main():
    sum = 0
    with open("input.txt", "r") as f:
        for line in f:
            rucksack = line.rstrip()
            half = len(rucksack)//2
            compartment1 = rucksack[:half]
            compartment2 = rucksack[half:]
            common_item_types = set(compartment1).intersection(compartment2)
            common_item_type = next(iter(common_item_types))
            priority = get_priority(common_item_type)
            sum += priority
    print(sum)

if __name__ == "__main__":
    main()
