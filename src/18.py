from collections import deque

dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
size = 71
byte_coords = [tuple(int(x) for x in line.split(","))
               for line in open(0).readlines()]


def solve(byte_count):
    corrupted_bytes = set(byte_coords[:byte_count])
    sx = sy = 0
    ex = ey = size - 1
    queue = deque([(sx, sy, 0)])
    seen = set()
    while queue:
        x, y, i = queue.pop()

        if (x, y) in seen:
            continue
        seen.add((x, y))

        if x == ex and y == ey:
            return i

        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy

            if (nx, ny) in corrupted_bytes or nx not in range(size) or ny not in range(size):
                continue

            queue.appendleft((nx, ny, i + 1))


print("Part 1:", solve(1024))

l, r = 0, len(byte_coords) - 1
while l < r:
    m = (l + r) // 2

    if solve(m) is not None:
        l = m + 1
    else:
        r = m
bx, by = byte_coords[l - 1]     # Last byte in the corrupt set
print("Part 2:", f"{bx},{by}")
