instructions = "".join(open(0))


def solve(instructions, use_conditionals):
    total = 0
    enable = True

    for i, _ in enumerate(instructions):
        current = instructions[i:]

        if use_conditionals and current.startswith("do()"):
            enable = True

        if use_conditionals and current.startswith("don't()"):
            enable = False

        if enable and current.startswith("mul("):
            current = current[4:]
            sep = current.find(",")
            end = current.find(")")

            if sep == -1 or end == -1:
                break

            first = current[:sep]
            second = current[sep + 1:end]

            if not first.isdecimal() or not second.isdecimal():
                continue

            total += int(first) * int(second)

    return total


print("Part 1:", solve(instructions, False))
print("Part 2:", solve(instructions, True))
