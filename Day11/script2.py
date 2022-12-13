from dataclasses import dataclass
from typing import Callable
from operator import add, mul

@dataclass
class Monkey:
    worry_levels: list[int]
    operation: Callable[[int], int]
    test: Callable[[int], bool]
    divisor: int
    true_target: int
    false_target: int
    inspections: int = 0

def main():
    with open("input.txt", "r") as f:
        lines = [line.rstrip() for line in f.readlines()]
    
    monkeys = read_monkeys(lines)
    divisors = [monkey.divisor for monkey in monkeys]
    divisors_mul = 1
    for divisor in divisors:
        divisors_mul *= divisor

    
    for round in range(10_000):
        print(round)
        if round == 20:
            print([monkey.inspections for monkey in monkeys])
            #break
        for monkey in monkeys:
            while monkey.worry_levels:
                monkey.inspections += 1
                worry_level = monkey.worry_levels.pop(0)
                worry_level = monkey.operation(worry_level)
                worry_level = worry_level % divisors_mul
                if monkey.test(worry_level):
                    monkeys[monkey.true_target].worry_levels.append(worry_level)
                else:
                    monkeys[monkey.false_target].worry_levels.append(worry_level)
    
    inspections = [monkey.inspections for monkey in monkeys]
    inspections.sort(reverse=True)
    print(inspections[0] * inspections[1])

def read_monkeys(lines: list[str]) -> list[Monkey]:
    monkeys = []
    producer = iter(lines)
    while (line := next(producer, None)) is not None:
        if line.startswith("Monkey "):
            worry_levels = [int(worry_level.strip()) for worry_level in get_value(next(producer)).split(",")]
            operation = get_operation(get_value(next(producer)))
            test, divisor = get_test(get_value(next(producer)))
            true_target = get_target(get_value(next(producer)))
            false_target = get_target(get_value(next(producer)))
            monkey = Monkey(worry_levels, operation, test, divisor, true_target, false_target)
            monkeys.append(monkey)
        elif line == "":
            continue
        else:
            raise Exception(f"Don't know what to do with line {line}")
    
    return monkeys

def get_value(line: str):
    return line.split(":")[1].strip()

def get_operation(text: str):
    text = text.split("=")[1].strip()
    return lambda old : operate(text, old)

def get_test(text: str):
    if text.startswith("divisible by "):
        divisor = int(text[len("divisible by "):])
        return lambda v : v % divisor == 0, divisor
    else:
        raise Exception(f"Don't know what to do with test expression {text}")

def get_target(text: str):
    if not text.startswith("throw to monkey "):
        raise Exception(f"Unknown target expression {text}")
    return int(text[len("throw to monkey "):])

def operate(text: str, old: int):
    parts = [part.strip() for part in text.split(" ")]
    left_str = parts[0]
    operator_str = parts[1]
    right_str = parts[2]
    
    left = make_number(left_str, old)
    right = make_number(right_str, old)
    if operator_str == "+":
        operator = add
    elif operator_str == "*":
        operator = mul
    else:
        raise Exception(f"Unknown operator {operator_str}")
    
    return operator(left, right)

def make_number(val: str, old: int):
    return old if val == "old" else int(val)

if __name__ == "__main__":
    #import cProfile
    #cProfile.run("main()")
    main()
