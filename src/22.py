def mix_and_prune(x, additional):
    return (x ^ additional) % 16777216


def gen_next(x):
    x = mix_and_prune(x, x * 64)
    x = mix_and_prune(x, x // 32)
    return mix_and_prune(x, x * 2048)


last_gen_count = 0
total_counter = {}
for initial in open(0).readlines():
    prev_num = int(initial)
    current_counter = {}

    sequence = (None, None, None, None)
    for i in range(2000):
        num = gen_next(prev_num)
        price = num % 10
        delta = price - (prev_num % 10)
        prev_num = num
        sequence = (delta, *sequence[:3])

        if i >= 3 and sequence not in current_counter:
            current_counter[sequence] = price

    last_gen_count += num
    for seq, amount in current_counter.items():
        total_counter[seq] = total_counter.get(seq, 0) + amount

print("Part 1:", last_gen_count)
print("Part 2:", max(total_counter.values()))
