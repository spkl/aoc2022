
def main():
    with open("input.txt") as f:
        grid = [line.rstrip() for line in f.readlines()]
    
    grid = [[int(height) for height in row] for row in grid]

    rows = len(grid)
    columns = len(grid[0])

    scenic_scores = [[-1 for _ in range(columns)] for _ in range(rows)]
    for row in range(rows):
        for column in range(columns):
            scenic_scores[row][column] = get_scenic_score(grid, row, column)
    
    max_scenic_score = max(max(tree_row) for tree_row in scenic_scores)
    print(scenic_scores)
    print(max_scenic_score)

def get_scenic_score(grid, row, column):
    if row == 0 \
        or column == 0 \
        or row == len(grid) - 1 \
        or column == len(grid[row]) - 1:
        return 0
    return get_left_viewing_distance(grid, row, column) \
        * get_top_viewing_distance(grid, row, column) \
        * get_right_viewing_distance(grid, row, column) \
        * get_bottom_viewing_distance(grid, row, column)

def get_left_viewing_distance(grid, row, column):
    my_height = grid[row][column]
    viewing_distance = 0
    for their_height in grid[row][column-1::-1]:
        viewing_distance += 1
        if their_height >= my_height:
            break
    return viewing_distance

def get_top_viewing_distance(grid, row, column):
    my_height = grid[row][column]
    viewing_distance = 0
    for upper_row in grid[row-1::-1]:
        viewing_distance += 1
        their_height = upper_row[column]
        if their_height >= my_height:
            break
    return viewing_distance

def get_right_viewing_distance(grid, row, column):
    my_height = grid[row][column]
    viewing_distance = 0
    for their_height in grid[row][column+1::]:
        viewing_distance += 1
        if their_height >= my_height:
            break
    return viewing_distance

def get_bottom_viewing_distance(grid, row, column):
    my_height = grid[row][column]
    viewing_distance = 0
    for lower_row in grid[row+1::]:
        viewing_distance += 1
        their_height = lower_row[column]
        if their_height >= my_height:
            break
    return viewing_distance

if __name__ == "__main__":
    main()