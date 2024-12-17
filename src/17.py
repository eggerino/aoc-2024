register_data, inst_data = open(0).read().split("\n\n")

registers = [int(x.split(": ")[1]) for x in register_data.splitlines()]
bytecode = list(int(x) for x in inst_data.split(": ")[1].split(","))


# Simulate machine
output_buf = []
inst_ptr = 0
while inst_ptr < len(bytecode) - 1:
    op_code = bytecode[inst_ptr]
    operand = bytecode[inst_ptr + 1]
    combo_operand = operand if operand < 4 else registers[operand - 4]

    if op_code == 0:
        registers[0] //= 2 ** combo_operand
    elif op_code == 1:
        registers[1] ^= operand
    elif op_code == 2:
        registers[1] = combo_operand % 8
    elif op_code == 3:
        if registers[0]:
            inst_ptr = operand - 2
    elif op_code == 4:
        registers[1] ^= registers[2]
    elif op_code == 5:
        output_buf.append(combo_operand % 8)
    elif op_code == 6:
        registers[1] = registers[0] // 2**combo_operand
    else:
        registers[2] = registers[0] // 2**combo_operand

    inst_ptr += 2

print("Part 1:", ",".join(map(str, output_buf)))

# Disassembled byte code:
# 2 4   -> B = A % 8
# 1 5   -> B = B ^ 5
# 7 5   -> C = A // 2**B
# 1 6   -> B = B ^ 6
# 0 3   -> A = A // 8
# 4 3   -> B = B ^ C
# 5 5   -> print(B % 8)
# 3 0   -> loop if a != 0

# Observations:
#
# - A will only be right shifted every iteration by 3 bits
#   A needs to be between 46-48 bits so the program produces 16 outputs
#
# - In every iteration B and C will be set before read.
#   Therefore all state is in A and none in B and C registers
#
# - Last iteration A is 1 - 3 bits (1-7)
#   Last iteration can be brute-forced
#
# - For second last iteration A is 4-6 (8-32)
#   Only the last 3 bits need to be found.
#   Higher bits are already required / determined by previous coming iterations
#   Only 8 must be brute-forced and checked for a valid output
#
# - No bits for previous iterations influence the output of the following iterations

# Solution:
#
# - Traverse the output in reverse order
# - Branch for every "node" of 3 digits
# - Check if the current "node" violates the required output and abort the traversal from the violating node
# - Branching factor from 8 is cut down siginificantly
# - Depth-first-search is feasable


def dfs(bytecode, a_acc):
    if not bytecode:
        return a_acc

    required_output = bytecode[-1]
    a_acc *= 8  # shift left by 3 bit

    for candidate in range(8):  # brute force all possible 3 bit digits
        a = a_acc + candidate   # simulate the one iteration of the program
        b = a % 8
        b = b ^ 5
        c = a // 2**b
        b = b ^ 6
        a = a // 8
        b = b ^ c

        actual_output = b % 8

        if required_output != actual_output:    # abort the node when a violation is found
            continue

        possible_a = dfs(bytecode[:-1], a_acc + candidate)
        # first found is also lowest since candidate are iterate increasing (with significance)
        if possible_a is not None:
            return possible_a

    return None


print("Part 2:", dfs(bytecode, 0))
