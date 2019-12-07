from itertools import permutations
from queue import Queue
from threading import Thread

logging = False
input_file = 'day7input.txt'

def get_param(state, mode, param):
    if mode == 0:
        return state[param]
    else:
        return param
def get_param(state, mode, param):
    if mode == 0:
        return state[param]
    else:
        return param


def run_instruction(state, pos, input_q, output_q):
    instruction = state[pos]
    param_mode1 = (instruction // 100) % 10
    param_mode2 = (instruction // 1000) % 10
    opcode = instruction % 100
    instruction_size = 0
    if opcode == 99:
        return None
    elif opcode == 1 or opcode == 2:
        instruction_size = 4
        if logging:
            print(pos, state[pos:pos+instruction_size])
        param1 = get_param(state, param_mode1, state[pos+1])
        param2 = get_param(state, param_mode2, state[pos+2])
        out = state[pos+3]
        if opcode == 1:
            state[out] = param1 + param2
        elif opcode == 2:
            state[out] = param1 * param2
    elif opcode == 3:
        instruction_size = 2
        if logging:
            print(pos, state[pos:pos+instruction_size])
        user_input = input_q.get(block=True)
        out = state[pos+1]
        state[out] = int(user_input)
    elif opcode == 4:
        instruction_size = 2
        if logging:
            print(pos, state[pos:pos+instruction_size])
        param1 = get_param(state, param_mode1, state[pos+1])
        output_q.put(param1)
    elif opcode == 5:
        instruction_size = 3
        if logging:
            print(pos, state[pos:pos+instruction_size])
        param1 = get_param(state, param_mode1, state[pos+1])
        param2 = get_param(state, param_mode2, state[pos+2])
        if param1 != 0:
            return param2
    elif opcode == 6:
        instruction_size = 3
        if logging:
            print(pos, state[pos:pos+instruction_size])
        param1 = get_param(state, param_mode1, state[pos+1])
        param2 = get_param(state, param_mode2, state[pos+2])
        if param1 == 0:
            return param2
    elif opcode == 7:
        instruction_size = 4
        if logging:
            print(pos, state[pos:pos+instruction_size])
        param1 = get_param(state, param_mode1, state[pos+1])
        param2 = get_param(state, param_mode2, state[pos+2])
        out = state[pos+3]
        if param1 < param2:
            state[out] = 1
        else:
            state[out] = 0
    elif opcode == 8:
        instruction_size = 4
        if logging:
            print(pos, state[pos:pos+instruction_size])
        param1 = get_param(state, param_mode1, state[pos+1])
        param2 = get_param(state, param_mode2, state[pos+2])
        out = state[pos+3]
        if param1 == param2:
            state[out] = 1
        else:
            state[out] = 0

    return pos + instruction_size


def execute(state, input_q, output_q):
    pos = 0
    while True:
        new_pos = run_instruction(state, pos, input_q, output_q)
        if new_pos is None:
            break
        pos = new_pos

def get_input():
    return [int(x) for x in open(input_file).read().split(',')]

def part1():
    strengths = []
    for perm in permutations([0, 1, 2, 3, 4]):
        output_q = Queue()
        output_q.put(0)
        for i, phase in enumerate(perm):
            state = get_input()
            input_q = Queue()
            input_q.put(phase)
            input_q.put(output_q.get())
            output_q = Queue()
            execute(state, input_q, output_q)
        strengths.append(output_q.get())

    return max(strengths)

def part2():
    strengths = []
    for perm in permutations([5, 6, 7, 8, 9]):
        pipes = [Queue() for _ in perm]

        states = [get_input() for _ in perm]

        for i, phase in enumerate(perm):
            pipes[i].put(phase)

        # Starting input
        pipes[0].put(0)

        threads = []
        for i, pipe in enumerate(pipes):
            threads.append(Thread(target=execute, args=(states[i], pipe, pipes[(i + 1) % 5])))

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        strengths.append(pipes[0].get())

    return max(strengths)

print(part1())
print(part2())
    

