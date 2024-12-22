from collections import deque

grid = [list(line.rstrip()) for line in open(0)]
rows = len(grid)
cols = len(grid[0])

for r, row in enumerate(grid):
    for c, tile in enumerate(row):
        if tile == "S":
            sr, sc = r, c
        elif tile == "E":
            er, ec = r, c


from_start = [[None for _ in range(cols)] for _ in range(rows)]
to_end = [[None for _ in range(cols)] for _ in range(rows)]


def fill_steps(tracker, r, c):
    q = deque([(r, c, 0)])
    while q:
        r, c, i = q.pop()

        if tracker[r][c] is not None:
            continue
        tracker[r][c] = i

        for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
            if nr not in range(rows) or nc not in range(cols) or grid[nr][nc] == "#":
                continue

            q.appendleft((nr, nc, i + 1))


def count_cheatable_paths(max_time, cheat_length):
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "#":
                continue

            for dr in range(-cheat_length, cheat_length + 1):
                for dc in range(-cheat_length, cheat_length + 1):
                    dist = abs(dr) + abs(dc)
                    if dist > cheat_length:
                        continue

                    nr = r + dr
                    nc = c + dc
                    if nr not in range(rows) or nc not in range(cols) or grid[nr][nc] == "#":
                        continue

                    time = to_end[nr][nc] + dist + from_start[r][c]
                    if time <= max_time:
                        count += 1

    return count


fill_steps(from_start, sr, sc)
fill_steps(to_end, er, ec)

max_time = from_start[er][ec] - 100
print("Part 1:", count_cheatable_paths(max_time, 2))
print("Part 2:", count_cheatable_paths(max_time, 20))
