GRID = [list(l.rstrip()) for l in open(0)]
ROWS = len(GRID)
COLS = len(GRID[0])


def solve_word(row, col):
    term = "XMAS"
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
            (0, 1), (1, -1), (1, 0), (1, 1)]

    total = 0
    for dr, dc in dirs:
        for i, val in enumerate(term):
            r = row + i * dr
            c = col + i * dc

            if r not in range(ROWS) or c not in range(COLS) or GRID[r][c] != val:
                break
        else:
            total += 1

    return total


def solve_cross(row, col):
    center = "A"
    other = set(("M", "S"))

    if row not in range(1, ROWS - 1) or col not in range(1, COLS - 1) or GRID[row][col] != center:
        return 0

    diag1 = [GRID[row - 1][col - 1], GRID[row + 1][col + 1]]
    diag2 = [GRID[row + 1][col - 1], GRID[row - 1][col + 1]]

    if len(other.intersection(diag1).intersection(diag2)) == 2:
        return 1
    else:
        return 0


total_word, total_cross = 0, 0
for r, row in enumerate(GRID):
    for c, _ in enumerate(row):
        total_word += solve_word(r, c)
        total_cross += solve_cross(r, c)
print("Part 1:", total_word)
print("Part 2:", total_cross)
