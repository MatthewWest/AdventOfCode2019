def get_param(state, mode, param):
    if mode == 0:
        return state[param]
    else:
        return param

def run_instruction(state, pos):
    opcode = state[pos]
    param_mode1 = (opcode // 100) % 10
    param_mode2 = (opcode // 1000) % 10
    opcode = opcode % 100
    instruction_size = 0
    if opcode == 99:
        return None
    elif opcode == 1 or opcode == 2:
        instruction_size = 4
        param1 = get_param(state, param_mode1, state[pos+1])
        param2 = get_param(state, param_mode2, state[pos+2])
        out = state[pos+3]
        if opcode == 1:
            state[out] = param1 + param2
        elif opcode == 2:
            state[out] = param1 * param2
    elif opcode == 3:
        instruction_size = 2
        user_input = input("enter input> ")
        out = state[pos+1]
        state[out] = int(user_input)
    elif opcode == 4:
        instruction_size = 2
        param1 = get_param(state, param_mode1, state[pos+1])
        print(param1)
    elif opcode == 5:
        instruction_size = 3
        param1 = get_param(state, param_mode1, state[pos+1])
        param2 = get_param(state, param_mode2, state[pos+2])
        if param1 != 0:
            return param2
    elif opcode == 6:
        instruction_size = 3
        param1 = get_param(state, param_mode1, state[pos+1])
        param2 = get_param(state, param_mode2, state[pos+2])
        if param1 == 0:
            return param2
    elif opcode == 7:
        instruction_size = 4
        param1 = get_param(state, param_mode1, state[pos+1])
        param2 = get_param(state, param_mode2, state[pos+2])
        out = state[pos+3]
        if param1 < param2:
            state[out] = 1
        else:
            state[out] = 0
    elif opcode == 8:
        instruction_size = 4
        param1 = get_param(state, param_mode1, state[pos+1])
        param2 = get_param(state, param_mode2, state[pos+2])
        out = state[pos+3]
        if param1 == param2:
            state[out] = 1
        else:
            state[out] = 0        

    return pos + instruction_size


def execute(state):
    pos = 0
    while True:
        new_pos = run_instruction(state, pos)
        # print(instruction_size, state)
        if new_pos is None:
            break
        pos = new_pos


def part1_or_part2():
    print('Enter 1 as input for part 1, enter 5 as input for part 2.')
    state = [int(x) for x in open('day5input.txt').read().split(',')]
    execute(state)


part1_or_part2()
