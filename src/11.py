from collections import Counter, defaultdict

stones = Counter(map(int, input().split()))


def blink(stones):
    new_stones = defaultdict(lambda: 0)
    for stone, amount in stones.items():
        stone_str = str(stone)
        stone_len = len(stone_str)

        if stone == 0:
            new_stones[1] += amount

        elif stone_len % 2 == 0:
            new_stones[int(stone_str[:stone_len // 2])] += amount
            new_stones[int(stone_str[stone_len // 2:])] += amount

        else:
            new_stones[stone * 2024] += amount

    return new_stones


for _ in range(25):
    stones = blink(stones)
print("Part 1:", sum(stones.values()))

for _ in range(50):
    stones = blink(stones)
print("Part 2:", sum(stones.values()))
