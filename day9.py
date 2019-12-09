from intcodecomputer import IntCodeComputer
from queue import Queue

s1 = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
s2 = '1102,34915192,34915192,7,4,7,99,0'
s3 = '104,1125899906842624,99'

def get_input():
  s = open('day9input.txt').read()
  return parse_input(s)

def parse_input(s):
    return [int(x) for x in s.split(',')]

def part1():
  in_q = Queue()
  in_q.put(1)
  out_q = Queue()
  comp = IntCodeComputer(get_input(), in_q, out_q)

  comp.execute()

  while not out_q.empty():
    print(out_q.get())

def part2():
  in_q = Queue()
  in_q.put(2)
  out_q = Queue()
  comp = IntCodeComputer(get_input(), in_q, out_q)

  comp.execute()

  while not out_q.empty():
    print(out_q.get())

part1()
part2()
