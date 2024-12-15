from collections import deque

data = open(0).read()
level, instructions = data.split("\n\n")

dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
instruction_map = {"^": 0, ">": 1, "v": 2, "<": 3}
moves = [instruction_map[i] for i in instructions if i in instruction_map]


def parse_level(level, wide):
    robot = (0, 0)
    boxes = set()
    walls = set()
    for r, row in enumerate(level.splitlines()):
        for c, tile in enumerate(row):
            if wide:
                c *= 2

            if tile == "@":
                robot = (r, c)
            elif tile == "O":
                boxes.add((r, c))
            elif tile == "#":
                walls.add((r, c))
                if wide:
                    walls.add((r, c + 1))

    return robot, boxes, walls


def move_robot(robot, boxes, walls, wide, moves):
    boxes = set(boxes)
    for m in moves:
        rr, rc = robot
        dr, dc = dirs[m]

        nr = rr + dr
        nc = rc + dc

        hit_wall = False
        queue = deque([(nr, nc)])
        moving_boxes = set()
        while queue:
            pr, pc = queue.popleft()

            if (pr, pc) in walls:
                hit_wall = True
                break

            if (pr, pc) in boxes and (pr, pc) not in moving_boxes:
                moving_boxes.add((pr, pc))
                queue.append((pr + dr, pc + dc))
                if wide:
                    queue.append((pr + dr, pc + dc + 1))

            if wide and (pr, pc - 1) in boxes and (pr, pc - 1) not in moving_boxes:
                moving_boxes.add((pr, pc - 1))
                queue.append((pr + dr, pc + dc - 1))
                queue.append((pr + dr, pc + dc))

        if hit_wall:
            continue

        robot = (nr, nc)

        for br, bc in moving_boxes:
            boxes.remove((br, bc))
        for br, bc in moving_boxes:
            boxes.add((br + dr, bc + dc))

    return boxes


def get_gps_sum(boxes):
    return sum(100 * r + c for r, c in boxes)


print("Part 1:", get_gps_sum(move_robot(*parse_level(level, False), False, moves)))
print("Part 2:", get_gps_sum(move_robot(*parse_level(level, True), True, moves)))
