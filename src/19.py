from collections import defaultdict
from functools import cache

towels, patterns = open(0).read().split("\n\n")

choices = defaultdict(list)
for towel in towels.split(", "):
    choices[towel[0]].append(towel)


@cache
def get_possibility_count(pattern):
    if not pattern:
        return 1

    count = 0
    for candidate in choices[pattern[0]]:
        if candidate == pattern[:len(candidate)]:
            count += get_possibility_count(pattern[len(candidate):])
    return count


counts = [get_possibility_count(pattern) for pattern in patterns.splitlines()]

print("Part 1:", sum(1 for c in counts if c > 0))
print("Part 2:", sum(counts))
