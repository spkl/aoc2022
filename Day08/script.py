
def main():
    with open("input.txt") as f:
        grid = [line.rstrip() for line in f.readlines()]
    
    grid = [[int(height) for height in row] for row in grid]

    rows = len(grid)
    columns = len(grid[0])

    visibility = [[False for _ in range(columns)] for _ in range(rows)]
    for row in range(rows):
        for column in range(columns):
            visibility[row][column] = is_tree_visible(grid, row, column)
    
    visible_trees = sum(sum(tree_row) for tree_row in visibility)
    print(visible_trees)

def is_tree_visible(grid, row, column):
    if row == 0 \
        or column == 0 \
        or row == len(grid) - 1 \
        or column == len(grid[row]) - 1:
        return True
    return is_inner_tree_visible_from_left(grid, row, column) \
        or is_inner_tree_visible_from_top(grid, row, column) \
        or is_inner_tree_visible_from_right(grid, row, column) \
        or is_inner_tree_visible_from_bottom(grid, row, column)

def is_inner_tree_visible_from_left(grid, row, column):
    my_height = grid[row][column]
    for their_height in grid[row][column-1::-1]:
        if their_height >= my_height:
            return False
    return True

def is_inner_tree_visible_from_top(grid, row, column):
    my_height = grid[row][column]
    for upper_row in grid[row-1::-1]:
        their_height = upper_row[column]
        if their_height >= my_height:
            return False
    return True

def is_inner_tree_visible_from_right(grid, row, column):
    my_height = grid[row][column]
    for their_height in grid[row][column+1::]:
        if their_height >= my_height:
            return False
    return True

def is_inner_tree_visible_from_bottom(grid, row, column):
    my_height = grid[row][column]
    for lower_row in grid[row+1::]:
        their_height = lower_row[column]
        if their_height >= my_height:
            return False
    return True

if __name__ == "__main__":
    main()