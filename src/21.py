from collections import deque
from functools import cache

num_keys = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [None, "0", "A"],
]
dir_keys = [
    [None, "^", "A"],
    ["<", "v", ">"],
]


def build_possibility_dict(keys):
    pos_dict = {}

    for sr, srow in enumerate(keys):
        for sc, stile in enumerate(srow):
            if stile is None:
                continue

            for er, erow in enumerate(keys):
                for ec, etile in enumerate(erow):
                    if etile is None:
                        continue

                    if stile == etile:
                        pos_dict[(stile, etile)] = ["A"]
                        continue

                    pos = []
                    q = deque([(sr, sc, "")])
                    min_path_len = 100
                    while q:
                        r, c, path = q.popleft()

                        if len(path) > min_path_len:
                            break

                        if (r, c) == (er, ec):
                            min_path_len = len(path)
                            pos.append(path + "A")

                        for nr, nc, dpath in [(r + 1, c, "v"), (r - 1, c, "^"), (r, c + 1, ">"), (r, c - 1, "<")]:
                            if nr not in range(len(keys)) or nc not in range(len(keys[0])) or keys[nr][nc] is None:
                                continue
                            q.append((nr, nc, path + dpath))

                    pos_dict[(stile, etile)] = pos

    return pos_dict


num_pos = build_possibility_dict(num_keys)
dir_pos = build_possibility_dict(dir_keys)


@cache
def solve(code, use_num, level):
    pos = num_pos if use_num else dir_pos

    total = 0
    for src, dest in zip("A" + code, code):
        cur_pos = pos[(src, dest)]

        if level == 0:
            total += len(cur_pos[0])
        else:
            total += min(solve(x, False, level - 1) for x in cur_pos)

    return total


total_2 = total_25 = 0
for code in open(0).read().splitlines():
    numeric = int(code.replace("A", ""))
    total_2 += solve(code, True, 2) * numeric
    total_25 += solve(code, True, 25) * numeric
print("Part 1:", total_2)
print("Part 2:", total_25)
