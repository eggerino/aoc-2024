disk = [int(x) for x in open(0).read().rstrip()]


def sum_up_exclusive(n):
    return n * (n - 1) // 2


def get_checksum(ptr, size, id):
    return id * (sum_up_exclusive(ptr + size) - sum_up_exclusive(ptr))


files = [x for i, x in enumerate(disk) if i % 2 == 0]
free_spaces = [x for i, x in enumerate(disk) if i % 2 == 1]

checksum = 0
i_consume = len(files) - 1
ptr = files[0]
for i_file in range(1, len(files)):
    i_free_space = i_file - 1

    free_space = free_spaces[i_free_space]

    # Fill up the free space with whole chunks of files
    while free_space > files[i_consume] and i_consume > i_free_space:
        checksum += get_checksum(ptr, files[i_consume], i_consume)
        ptr += files[i_consume]

        free_space -= files[i_consume]
        files[i_consume] = 0
        i_consume -= 1

    if i_consume == i_free_space:
        break   # every thing is done

    # Fill the remaining free space with a partial file
    checksum += get_checksum(ptr, free_space, i_consume)
    ptr += free_space
    files[i_consume] -= free_space

    # the current file stays in place
    checksum += get_checksum(ptr, files[i_file], i_file)
    ptr += files[i_file]

print("Part 1:", checksum)

ptr = 0
files = []
free_spaces = []
for i, space in enumerate(disk):
    if i % 2 == 1:
        free_spaces.append([ptr, space])
    else:
        files.append([ptr, space, i // 2])

    ptr += space

for i in reversed(range(len(files))):
    _, file_size, _ = files[i]
    for i_spaces, [space_ptr, space_size] in enumerate(free_spaces):
        if i_spaces == i:
            break
        if space_size >= file_size:
            files[i][0] = space_ptr
            free_spaces[i_spaces] = [space_ptr + file_size, space_size - file_size]
            break

print("Part 2:", sum(get_checksum(*x) for x in files))
