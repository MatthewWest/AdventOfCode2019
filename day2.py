
def execute(noun, verb):
    state = [int(x) for x in open('day2input.txt').read().split(',')]

    state[1] = noun
    state[2] = verb
    pos = 0
    while True:
        opcode = state[pos]
        if opcode == 99:
            break
        else:
            in1 = state[pos+1]
            in2 = state[pos+2]
            out = state[pos+3]
            if opcode == 1:
                state[out] = state[in1] + state[in2]
            elif opcode == 2:
                state[out] = state[in1] * state[in2]
        pos += 4

    return state[0]

def find_target(target):
    for x in range(0, 100):
        for y in range(0, 100):
            if execute(x, y) == target:
                return x*100 + y

def part1():
    return execute(12, 2)

def part2():
    return find_target(19690720)

print(part1())
print(part2())
