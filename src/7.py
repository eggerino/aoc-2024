def can_evaluate_to(result, operands, allow_concat):
    if len(operands) == 1:
        return result == operands[0]

    if result % operands[-1] == 0 and can_evaluate_to(result // operands[-1], operands[:-1], allow_concat):
        return True

    if result > operands[-1] and can_evaluate_to(result - operands[-1], operands[:-1], allow_concat):
        return True

    result_str = str(result)
    last_str = str(operands[-1])
    can_concat = len(result_str) > len(last_str) and result_str.endswith(last_str)
    if allow_concat and can_concat and can_evaluate_to(int(result_str[:-len(last_str)]), operands[:-1], allow_concat):
        return True

    return False


total, total_concat = 0, 0
for line in open(0):
    test, operands = line.split(": ")
    test = int(test)
    operands = list(map(int, operands.split(" ")))

    if can_evaluate_to(test, operands, False):
        total += test

    if can_evaluate_to(test, operands, True):
        total_concat += test

print("Part 1:", total)
print("Part 2:", total_concat)
