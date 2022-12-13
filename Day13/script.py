import ast

def main():
    with open("input.txt", "r") as f:
        lines = [line.rstrip() for line in f.readlines()]
    
    lines = iter(lines)
    pairs = []
    sentinel = object()
    while (line := next(lines, sentinel)) != sentinel:
        if line == "":
            continue
        left = ast.literal_eval(line)
        right = ast.literal_eval(next(lines))
        pairs.append((left, right))

    sum = 0
    for index, (left, right) in enumerate(pairs, 1):
        if check_order(left, right):
            sum += index
    
    print(sum)

def check_order(left, right):
    if isinstance(left, int) and isinstance(right, int):
        return check_order_int(left, right)
    
    if isinstance(left, list) and isinstance(right, list):
        return check_order_list(left, right)
    
    left = ensure_list(left)
    right = ensure_list(right)
    return check_order(left, right)
        
def check_order_int(left_int, right_int):
    if left_int < right_int:
        return True
    if left_int > right_int:
        return False
    return None

def check_order_list(left_list, right_list):
    for left, right in zip(left_list, right_list):
        result = check_order(left, right)
        if result is not None:
            return result
    
    if len(left_list) < len(right_list):
        return True
    elif len(left_list) > len(right_list):
        return False
    return None

def ensure_list(item):
    if not isinstance(item, list):
        return [item]
    return item

if __name__ == "__main__":
    main()
