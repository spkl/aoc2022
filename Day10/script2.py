from itertools import count
from enum import Enum

class State(Enum):
    READY = 0
    PROCESS_ADDX = 1

def main():
    with open("input.txt", "r") as f:
        instructions = [line.rstrip() for line in f.readlines()]
    
    X = 1
    state = State.READY
    instruction = None
    pixel = 0
    for cycle in count(1):
        if pixel in (X - 1, X, X + 1):
            print("#", end="")
        else:
            print(".", end="")

        if pixel == 39:
            pixel = 0
            print()
        else:
            pixel += 1
        
        if state == State.READY:
            if not instructions:
                break
            instruction = instructions.pop(0)
            if instruction == "noop":
                pass
            elif instruction.startswith("addx"):
                state = State.PROCESS_ADDX
        elif state == State.PROCESS_ADDX:
            V = int(instruction.split(" ")[1])
            X += V
            state = State.READY
        else:
            raise Exception(f"Unknown state {state}")

if __name__ == "__main__":
    main()
