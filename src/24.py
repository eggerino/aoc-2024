from functools import cache
from itertools import chain


def create_gate(op, first_source, second_source):
    return op, *sorted((first_source, second_source))


def numbered(label, index):
    return f"{label}{index:02d}"


inits_def, gates_def = open(0).read().split("\n\n")

inits = {}
for line in inits_def.splitlines():
    wire, value = line.split(": ")
    inits[wire] = value == "1"

gate_for = {}
wire_of = {}
for line in gates_def.splitlines():
    src1, op, src2, _, dest = line.split(" ")
    gate = create_gate(op, src1, src2)
    gate_for[dest] = gate
    wire_of[gate] = dest

all_wires = chain(inits.keys(), gate_for.keys())
num_z_wires = sum(1 for wire in all_wires if wire.startswith("z"))


@cache
def get_value_of(wire):
    if wire in inits:
        return inits[wire]
    
    op, src1, src2 = gate_for[wire]
    val1 = get_value_of(src1)
    val2 = get_value_of(src2)
    
    if op == "AND":
        return val1 and val2
    elif op == "OR":
        return val1 or val2
    elif op == "XOR":
        return val1 != val2


number = 0
for i in reversed(range(num_z_wires)):
    number *= 2
    number += int(get_value_of(numbered("z", i)))
print("Part 1:", number)


swaps = []


def swap(first_wire, second_wire):
    swaps.extend((first_wire, second_wire))
    first_gate = gate_for[first_wire]
    second_gate = gate_for[second_wire]
    gate_for[first_wire] = second_gate
    gate_for[second_wire] = first_gate
    wire_of[first_gate] = second_wire
    wire_of[second_gate] = first_wire


# Part 2 uses some assumption of the dataset
# 1. x00 and y00 build a half adder of the following architecture:
# x00 --+----->+-----+
#       |      | xor |>-- z00
# y00 --v--+-->+-----+
#       |  |
#       |  +-->+-----+
#       |      | and |>-- carry
#       +----->+-----+
#
# 2. xi and yi build a full adder of the following architecture:
# xi    --+----->+-----+
#         |      | xor |>-----+-->+-----+
# yi    --v--+-->+-----+      |   | xor |>------------- zi
#         |  |                |   |     |
# carry --v--v-------------+--v-->+-----+
#         |  |             |  |
#         |  |             |  +-->+-----+
#         |  |             |      | and |>-->+-----+
#         |  |             +----->+-----+    |     |
#         |  |                               |  or |>-- carry
#         |  +------------------->+-----+    |     |
#         |                       | and |>-->+-----+
#         +---------------------->+-----+
#
# 3. A maximum of one error occures per adder circuit,
#    while the carry is considered to be part of the following circuit
#    -> Carry is check as carry in and not as carry out
#
# 4. Last bit is just the last carry (out)
#
# 5. There are no noop gates like abc AND abc to obfuscate the circuit

# check the half adder for the 0.th bit
z = wire_of[("XOR", "x00", "y00")]
if z != "z00":
    swap(z, "z00")
carry = wire_of[("AND", "x00", "y00")]

# check all full adders for the i-th bit (excluding the last bit (is carry))
for i in range(1, num_z_wires - 1):
    x = numbered("x", i)
    y = numbered("y", i)
    z = numbered("z", i)

    z_op, *z_srcs = gate_for[z]
    abx = wire_of[("XOR", x, y)]

    if z_op != "XOR" or (abx not in z_srcs and carry not in z_srcs):
        # Last xor is wrong
        swap(z, wire_of[create_gate("XOR", abx, carry)])

    elif carry not in z_srcs:
        # carry in is wrong
        actual_carry, = (x for x in z_srcs if x != abx)
        swap(carry, actual_carry)
        carry = actual_carry

    elif abx not in z_srcs:
        # First xor is wrong
        actual_abx, = (x for x in z_srcs if x != carry)
        swap(abx, actual_abx)

    else:
        # No error in the xor gates
        # check the two and gates

        ab = wire_of[("AND", x, y)]
        abc = wire_of[create_gate("AND", abx, carry)]

        possible_ors = [gate for gate in gate_for.values() if gate[0] == "OR" and (ab in gate[1:] or abc in gate[1:])]
        assert len(possible_ors) == 1
        or_gate = possible_ors[0]

        if ab not in or_gate:
            actual_ab = next(src for src in or_gate[1:] if src != abc)
            swap(ab, actual_ab)
        elif abc not in or_gate:
            actual_abc = next(src for src in or_gate[1:] if src != ab)
            swap(abc, actual_abc)
    
    # Recompute the carry out wire with the possibly swapped full adder
    abx = wire_of[("XOR", x, y)]
    abc = wire_of[create_gate("AND", abx, carry)]
    ab = wire_of[("AND", x, y)]
    carry = wire_of[create_gate("OR", abc, ab)]

# check for the last carry
z = numbered("z", num_z_wires - 1)
if z != carry:
    swap(z, carry)

print("Part 2:", ",".join(sorted(swaps)))
