def read_values(line, premarker):
    _, a, b = line.split(premarker)
    return map(int, [a.split(",")[0], b])


def get_minimum_tokens(a, b, r):
    # Solve linear system of equations
    # Only allow integer solutions
    # ax * na + bx * nb = rx
    # ay * na + by * nb = ry
    # [a, b] * n = r
    ax, ay = a
    bx, by = b
    rx, ry = r
    det = ax * by - ay * bx

    if det == 0:
        # a and b are parallel
        # There are ether no or infinte many solutions
        # in the infinite case only choosing one button will yield the minimum
        # since every combination of buttons is in between the cost
        # The extrema are at the pure strategies
        na = rx // ax
        nb = rx // bx
        tokens = []
        if ax * na == rx and ay * na == ry:
            tokens.append(na * 3)
        if bx * nb == rx and by * nb == ry:
            tokens.append(nb)
        return min(tokens) if tokens else 0

    else:
        # matrix is invertable -> exactly one solution
        # only except the solution if it's an integer and positive
        na = (by * rx - bx * ry) // det
        nb = (-ay * rx + ax * ry) // det
        if na > 0 and nb > 0 and ax * na + bx * nb == rx and ay * na + by * nb == ry:
            return 3 * na + nb

    return 0


data = open(0).read()

total, total_calib = 0, 0
for description in data.split("\n\n"):
    a_line, b_line, r_line = description.splitlines()
    a = list(read_values(a_line, "+"))
    b = list(read_values(b_line, "+"))
    r = list(read_values(r_line, "="))
    r_calib = map(lambda x: x + 10000000000000, r)
    total += get_minimum_tokens(a, b, r)
    total_calib += get_minimum_tokens(a, b,  r_calib)

print("Part 1:", total)
print("Part 2:", total_calib)
