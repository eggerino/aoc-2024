import heapq
from collections import defaultdict, deque

grid = [line.rstrip() for line in open(0)]

for r, row in enumerate(grid):
    for c, tile in enumerate(row):
        if tile == "S":
            sr, sc = r, c

best_cost = float("inf")
queue = [(0, (sr, sc, 0, 1), None)]
came_from = defaultdict(set)
best_costs = defaultdict(lambda: float("inf"))

while queue:
    cost, current, previous = heapq.heappop(queue)
    r, c, dr, dc = current

    if cost > best_cost:
        break

    if grid[r][c] == "E":
        best_cost = cost
        er, ec = r, c

    if cost > best_costs[current]:
        continue
    best_costs[current] = cost

    came_from[current].add(previous)

    for ncost, nr, nc, ndr, ndc in [(cost + 1, r + dr, c + dc, dr, dc), (cost + 1000, r, c, -dc, dr), (cost + 1000, r, c, dc, -dr)]:
        if grid[nr][nc] == "#" or ncost > best_costs[(nr, nc, ndr, ndc)]:
            continue
        heapq.heappush(queue, (ncost, (nr, nc, ndr, ndc), current))

print("Part 1:", best_cost)

best_tiles = set()
for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
    queue = deque([(er, ec, dr, dc)])
    while queue:
        r, c, dr, dc = queue.pop()
        best_tiles.add((r, c))
        for previous in came_from[(r, c, dr, dc)]:
            if previous is not None:
                queue.appendleft(previous)
print("Part 2;", len(best_tiles))
