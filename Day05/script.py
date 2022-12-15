import re

def main():
    reading_stacks = True
    stacks = [list() for _ in range(9)]
    with open("input.txt") as f:
        for line in f:
            line = line.rstrip()
            
            if line.startswith(" 1"):
                continue

            if reading_stacks and not line:
                reading_stacks = False
                for stack in stacks:
                    stack.reverse()
                continue
            
            if reading_stacks:
                for idx, stack in enumerate(stacks):
                    column = 1 + idx * 4
                    if len(line) < column:
                        break
                    else:
                        symbol = line[column]
                        if symbol == " ":
                            continue
                        stack.append(symbol)
            else:
                count, source, target = re.findall("[0-9]+", line)
                count, source, target = int(count), int(source), int(target)
                for _ in range(count):
                    stacks[target - 1].append(stacks[source - 1].pop())

    result = ""
    for stack in stacks:
        if stack:
            result += stack[-1]
    print(result)

if __name__ == "__main__":
    main()