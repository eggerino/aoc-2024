from functools import lru_cache

GRID = [list(map(int, line.rstrip())) for line in open(0)]
ROWS = len(GRID)
COLS = len(GRID[0])

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def get_score(row, col):
    def dfs(row, col, ends):
        if GRID[row][col] == 9:
            ends.add((row, col))
            return ends

        for dr, dc in DIRS:
            r = row + dr
            c = col + dc
            if r in range(ROWS) and c in range(COLS) and GRID[r][c] == 1 + GRID[row][col]:
                dfs(r, c, ends)
        return ends
    return len(dfs(row, col, set()))


@lru_cache
def get_rating(row, col):
    if GRID[row][col] == 9:
        return 1

    score = 0
    for dr, dc in DIRS:
        r = row + dr
        c = col + dc
        if r in range(ROWS) and c in range(COLS) and GRID[r][c] == 1 + GRID[row][col]:
            score += get_rating(r, c)
    return score


total_score, total_rating = 0, 0
for r, row in enumerate(GRID):
    for c, tile in enumerate(row):
        if tile == 0:
            total_score += get_score(r, c)
            total_rating += get_rating(r, c)

print("Part 1:", total_score)
print("Part 2:", total_rating)
