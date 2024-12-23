from collections import defaultdict

graph = defaultdict(set)
for connection in open(0):
    src, dest = connection.rstrip().split("-")
    graph[src].add(dest)
    graph[dest].add(src)

count = 0
triples = set()
for src, dests in graph.items():
    for dest in dests:
        next_dests = graph[dest]
        intersection = next_dests.intersection(dests)

        if not intersection:
            continue

        for other in intersection:
            if "t" in src[0] + dest[0] + other[0]:
                count += 1
print("Part 1:", count // 6)


def find_max_clique():
    maxima = []

    def bron_kerbosch(r: set, p: set, x: set):
        if not p and not x:
            maxima.append(r)
            return

        vertices = list(p)
        for v in vertices:
            set_v = set([v])
            n_v = graph[v]

            bron_kerbosch(r.union(set_v), p.intersection(n_v), x.intersection(n_v))

            p.remove(v)
            x.add(v)

    bron_kerbosch(set(), set(graph.keys()), set())
    return max(maxima, key=len)


print("Part 2:", ",".join(sorted(find_max_clique())))
