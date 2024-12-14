xsize = 101
ysize = 103


def parse_robot(line):
    return map(lambda x: map(int, x.split("=")[1].split(",")), line.split(" "))


robots = []
for robot in open(0):
    (px, py), (vx, vy) = parse_robot(robot)
    robots.append((px, py, vx, vy))


def get_safety_factor(second):
    q1, q2, q3, q4 = 0, 0, 0, 0
    for px, py, vx, vy in robots:
        px += vx * second
        px = px % xsize
        py += vy * second
        py = py % ysize

        if px in range(xsize // 2) and py in range(ysize // 2):
            q1 += 1
        elif px in range(xsize // 2) and py in range(ysize // 2 + 1, ysize):
            q2 += 1
        elif px in range(xsize // 2 + 1, xsize) and py in range(ysize // 2):
            q3 += 1
        elif px in range(xsize // 2 + 1, xsize) and py in range(ysize // 2 + 1, ysize):
            q4 += 1

    return q1 * q2 * q3 * q4


print("Part 1:", get_safety_factor(100))

min_factor = float("inf")
min_second = -1
for s in range(xsize * ysize):
    factor = get_safety_factor(s)
    if factor < min_factor:
        min_factor = factor
        min_second = s
print("Part 2:", min_second)
