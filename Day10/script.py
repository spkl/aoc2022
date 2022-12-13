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
    total_signal_strength = 0
    instruction = None
    for cycle in count(1):
        if (cycle - 20) % 40 == 0:
            signal_strength = cycle * X
            print(signal_strength)
            total_signal_strength += signal_strength

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

    print(total_signal_strength)

if __name__ == "__main__":
    main()
