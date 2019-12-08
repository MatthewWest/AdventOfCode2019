from itertools import permutations
from queue import Queue
from threading import Thread
from intcodecomputer import IntCodeComputer

input_file = 'day7input.txt'


def get_input():
    return [int(x) for x in open(input_file).read().split(',')]

def part1():
    strengths = []
    for perm in permutations([0, 1, 2, 3, 4]):
        output_q = Queue()
        output_q.put(0)
        for i, phase in enumerate(perm):
            input_q = Queue()
            input_q.put(phase)
            input_q.put(output_q.get())
            output_q = Queue()
            computer = IntCodeComputer(get_input(), input_q, output_q)
            computer.execute()
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

        computers = []
        for i, state in enumerate(states):
            computers.append(IntCodeComputer(state, pipes[i], pipes[(i+1)%5]))


        threads = []
        for computer in computers:
            threads.append(Thread(target=computer.execute))

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        strengths.append(pipes[0].get())

    return max(strengths)

print(part1())
print(part2())
    

