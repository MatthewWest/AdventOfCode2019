from intcodecomputer import IntCodeComputer
from queue import Queue


def get_input():
  return parse_input(open('day21input.txt').read())

def parse_input(s):
    return [int(x) for x in s.split(',')]


def input_line(s: str, in_q: Queue):
  for c in s:
    in_q.put(ord(c))
  in_q.put(ord('\n'))


def print_output(out_q):
  line = []
  while not out_q.empty():
    out = out_q.get()
    if out <= 255:
      c = chr(out)
    else:
      print(out)
      return
    if c == '\n':
      print(''.join(line))
      line = []      
    else:
      line.append(c)
  print(''.join(line))
  return


def part1():
  in_q = Queue()
  out_q = Queue()
  comp = IntCodeComputer(get_input(), in_q, out_q)

  program = [
    # 3-wide hole -> J
    'NOT A J',
    'NOT B T',
    'AND T J',
    'NOT C T',
    'AND T J',
    'AND D J',
    # Three after is a hole
    'NOT C T',
    'OR T J',
    # One after is a hole
    'NOT A T',
    'OR T J',
    # ground 4 squares in front
    'AND D J',
    'WALK'
  ]
  for line in program:
    input_line(line, in_q)

  comp.execute(blocking=False)
  print_output(out_q)


def part2():
  in_q = Queue()
  out_q = Queue()
  comp = IntCodeComputer(get_input(), in_q, out_q)

  # (D && !(A && B && (C || !H)))
  # mostly represented right to left
  program = [
    'NOT H T',
    'OR C T',
    'AND B T',
    'AND A T',
    'NOT T J',  
    'AND D J',
    'RUN',
  ]
  for line in program:
    input_line(line, in_q)

  comp.execute(blocking=False)
print_output(out_q)
