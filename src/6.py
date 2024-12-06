LEVEL = [list(l.rstrip()) for l in open(0)]
ROWS = len(LEVEL)
COLS = len(LEVEL[0])
DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

OBJECTS = set()
guard = None
for r, row in enumerate(LEVEL):
    for c, tile in enumerate(row):
        if tile == "#":
            OBJECTS.add((r, c))
        if tile == "^":
            guard = (r, c)


def walk(start, objects):
    path = set()
    states = set()
    dir_idx = 0
    guard = start

    while True:
        path.add(guard)
        states.add((*guard, dir_idx))

        r, c = guard
        dr, dc = DIRS[dir_idx]
        pr, pc = r + dr, c + dc

        if not (pr in range(ROWS) and pc in range(COLS)):
            return path

        if (pr, pc) in objects:
            dir_idx += 1
            dir_idx = dir_idx % 4
        else:
            guard = pr, pc

        if (pr, pc, dir_idx) in states:
            return None


initial_path = walk(guard, OBJECTS)
print("Part 1:", len(initial_path))

total_loops = 0
initial_path.remove(guard)
for obj in initial_path:
    objects = set(OBJECTS)
    objects.add(obj)
    if not walk(guard, objects):
        total_loops += 1
print("Part 2:", total_loops)
