def is_safe(levels):
    diffs = [b - a for a, b in zip(levels, levels[1:])]
    return all(0 < diff < 4 for diff in diffs) or all(0 > diff > -4 for diff in diffs)


total_strict, total_tolerant = 0, 0
for report in open(0):
    levels = list(map(int, report.split()))

    if is_safe(levels):
        total_strict += 1

    if any(is_safe(levels[:i] + levels[i + 1:]) for i in range(len(levels))):
        total_tolerant += 1

print("Part 1:", total_strict)
print("Part 2:", total_tolerant)
