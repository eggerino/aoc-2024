from collections import defaultdict
from functools import cmp_to_key


rules_data, updates_data = open(0).read().rstrip().split("\n\n")

rules = defaultdict(set)
for line in rules_data.split("\n"):
    before, after = map(int, line.split("|"))
    rules[before].add(after)


def compare(a, b):
    if a in rules and b in rules[a]:
        return -1

    if b in rules and a in rules[b]:
        return 1

    return 0


total_ordered, total_unordered = 0, 0
for line in updates_data.split("\n"):
    updates = list(map(int, line.split(",")))

    if all(compare(a, b) < 0 for a, b in zip(updates, updates[1:])):
        total_ordered += updates[len(updates) // 2]
    else:
        updates = sorted(updates, key=cmp_to_key(compare))
        total_unordered += updates[len(updates) // 2]

print("Part 1:", total_ordered)
print("Part 2:", total_unordered)
