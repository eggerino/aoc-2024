from collections import deque, defaultdict

grid = [x.rstrip() for x in open(0).readlines()]
rows = len(grid)
cols = len(grid[0])
dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

seen = set()


def get_prices(row, col):
    tile = grid[row][col]
    area = 0
    fences = defaultdict(set)

    queue = deque([(row, col)])
    while queue:
        r, c = queue.popleft()

        if (r, c) in seen:
            continue
        seen.add((r, c))
        area += 1

        for dr, dc in dirs:
            nr = r + dr
            nc = c + dc

            if nr not in range(rows) or nc not in range(cols) or grid[nr][nc] != tile:
                fences[(dr, dc)].add((r, c))
            else:
                queue.append((nr, nc))

    sides = 0
    for edges in fences.values():
        seen_edges = set()
        for r, c in edges:
            if (r, c) in seen_edges:
                continue
            sides += 1

            queue = deque([(r, c)])
            while queue:
                r, c = queue.popleft()
                if (r, c) in seen_edges:
                    continue
                seen_edges.add((r, c))

                for dr, dc in dirs:
                    nr = r + dr
                    nc = c + dc
                    if (nr, nc) in edges:
                        queue.append((nr, nc))

    return area * sum(map(len, fences.values())), area * sides


total_fences, total_sides = 0, 0
for r, row in enumerate(grid):
    for c, _ in enumerate(row):
        if (r, c) in seen:
            continue
        price_fences, price_sides = get_prices(r, c)
        total_fences += price_fences
        total_sides += price_sides
print("Part 1:", total_fences)
print("Part 2:", total_sides)
