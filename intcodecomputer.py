from itertools import permutations
from queue import Queue
from threading import Thread

class IntCodeComputer:
    def __init__(self, mem, input_q, output_q, starting_pc=0):
        self._mem = mem + [0 for _ in range(100000)]
        self._pc = starting_pc
        self._input_q = input_q
        self._output_q = output_q
        self._halted = False
        self._relative_base = 0


    @property
    def halted(self):
        return self._halted
    

    def _get_param(self, mode, param):
        if mode == 0:
            return self._mem[param]
        elif mode == 1:
            return param
        elif mode == 2:
            return self._mem[param + self._relative_base]
        else:
            raise Exception("Illegal mode {:}".format(mode))

    def _get_output_address(self, mode, val):
        if mode == 0:
            return val
        elif mode == 1:
            raise Exception("Illegal use of immediate mode for an output parameter")
        elif mode == 2:
            return val + self._relative_base
        else:
            raise Exception("Illegal mode {:}".format(mode))

    def run_instruction(self, blocking=True):
        """Run a single instruction.

        Can block on the input queue if blocking is set to true."""
        instruction = self._mem[self._pc]
        p1_mode = (instruction // 100) % 10
        p2_mode = (instruction // 1000) % 10
        p3_mode = (instruction // 10000) % 10
        opcode = instruction % 100
        instruction_size = 0
        if opcode == 99:  # Halt
            self._halted = True
        elif opcode == 1 or opcode == 2:  # Add & Mul
            p1 = self._get_param(p1_mode, self._mem[self._pc+1])
            p2 = self._get_param(p2_mode, self._mem[self._pc+2])
            out = self._get_output_address(p3_mode, self._mem[self._pc+3])
            if opcode == 1:
                self._mem[out] = p1 + p2
            elif opcode == 2:
                self._mem[out] = p1 * p2
            self._pc += 4
        elif opcode == 3:  # Read Input
            out = self._get_output_address(p1_mode, self._mem[self._pc+1])
            self._mem[out] = int(self._input_q.get(block=blocking))
            self._pc += 2
        elif opcode == 4:  # Output
            p1 = self._get_param(p1_mode, self._mem[self._pc+1])
            self._output_q.put(p1)
            self._pc += 2
        elif opcode == 5:  # Jump if true
            p1 = self._get_param(p1_mode, self._mem[self._pc+1])
            p2 = self._get_param(p2_mode, self._mem[self._pc+2])
            if p1 != 0:
                self._pc = p2
            else:
                self._pc += 3
        elif opcode == 6:  # Jump if false
            p1 = self._get_param(p1_mode, self._mem[self._pc+1])
            p2 = self._get_param(p2_mode, self._mem[self._pc+2])
            if p1 == 0:
                self._pc = p2
            else:
                self._pc += 3
        elif opcode == 7:  # Less than
            p1 = self._get_param(p1_mode, self._mem[self._pc+1])
            p2 = self._get_param(p2_mode, self._mem[self._pc+2])
            out = self._get_output_address(p3_mode, self._mem[self._pc+3])
            if p1 < p2:
                self._mem[out] = 1
            else:
                self._mem[out] = 0
            self._pc += 4
        elif opcode == 8:  # Equal to
            p1 = self._get_param(p1_mode, self._mem[self._pc+1])
            p2 = self._get_param(p2_mode, self._mem[self._pc+2])
            out = self._get_output_address(p3_mode, self._mem[self._pc+3])
            if p1 == p2:
                self._mem[out] = 1
            else:
                self._mem[out] = 0
            self._pc += 4
        elif opcode == 9:  # move relative base
            p1 = self._get_param(p1_mode, self._mem[self._pc+1])
            self._pc += 2
            self._relative_base += p1
        else:
            raise Exception("Unrecognized instruction '{:}' at pc {:}\nmem[{:}:{:}] = {:}".format(instruction, self._pc, self._pc, self._pc+25, self._mem[self._pc:self._pc+25]))


    def execute(self, blocking=True):
        """Execute the intcode computer until it halts.

        If blocking is set to False, it will raise a queue.Empty exception if no input
        is available when an input instruction is requested"""
        while not self.halted:
            self.run_instruction(blocking)
