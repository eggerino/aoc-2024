from collections import Counter

list_one, list_two = [], []
for line in open(0).readlines():
    num_one, num_two = map(int, line.split())
    list_one.append(num_one)
    list_two.append(num_two)
list_one.sort()
list_two.sort()

total = 0
for num_one, num_two in zip(list_one, list_two):
    total += abs(num_one - num_two)

print("Part 1:", total)

total = 0
counter = Counter(list_two)
for num in list_one:
    total += num * counter.get(num, 0)

print("Part 2:", total)
