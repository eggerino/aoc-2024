from collections import defaultdict

GRID = open(0).read().splitlines()
ROWS = len(GRID)
COLS = len(GRID[0])

antennas = defaultdict(list)
for r, row in enumerate(GRID):
    for c, tile in enumerate(row):
        if tile == ".":
            continue
        antennas[tile].append((r, c))


def in_grid(x):
    r, c = x
    return r in range(ROWS) and c in range(COLS)


def get_antinodes(x, y):
    xr, xc = x
    yr, yc = y
    dr = xr - yr
    dc = xc - yc
    return filter(in_grid, [(xr + dr, xc + dc), (yr - dr, yc - dc)])


def get_antinodes_harmonics(x, y):
    xr, xc = x
    yr, yc = y
    dr = xr - yr
    dc = xc - yc

    antinodes = [x]
    for sign in [-1, 1]:
        a = x
        while in_grid(a):
            if a != x:
                antinodes.append(a)
            r, c = a
            a = r + sign * dr, c + sign * dc
    return antinodes


antinodes = set()
antinodes_harmonics = set()
for _, a in antennas.items():
    for i, first in enumerate(a):
        for second in a[i + 1:]:
            for antinode in get_antinodes(first, second):
                antinodes.add(antinode)
            for antinode in get_antinodes_harmonics(first, second):
                antinodes_harmonics.add(antinode)
print("Part 1:", len(antinodes))
print("Part 2:", len(antinodes_harmonics))
