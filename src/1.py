from collections import Counter

list_one, list_two = [], []
for line in open(0).readlines():
    num_one, num_two = map(int, line.split())
    list_one.append(num_one)
    list_two.append(num_two)
list_one.sort()
list_two.sort()

part1 = 0
for num_one, num_two in zip(list_one, list_two):
    part1 += abs(num_one - num_two)

print("Part 1:", part1)

part2 = 0
counter = Counter(list_two)
for num in list_one:
    part2 += num * counter.get(num, 0)

print("Part 2:", part2)
