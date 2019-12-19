from intcodecomputer import IntCodeComputer
from queue import Queue, Empty
from collections import defaultdict

input_file = 'day19input.txt'

def get_input():
    return [int(x) for x in open(input_file).read().split(',')]


mem = get_input()
input_q = Queue()
output_q = Queue()

def is_pulled(x, y):
  comp = IntCodeComputer(mem, input_q, output_q)
  input_q.put(x)
  input_q.put(y)
  comp.execute(blocking=False)
  res = output_q.get()
  if res == 1:
    return True
  else:
    return False



def part1():
  mem = get_input()

  m = defaultdict(lambda: ' ')
  for x in range(50):
    for y in range(50):
      if is_pulled(x, y):
        m[(x, y)] = '#'
      else:
        m[(x, y)] = '.'

  count = 0
  for p in m:
    if m[p] == '#':
      count += 1
  return count


def part2():
  x = 0
  y = 0
  while not is_pulled(x+99, y):
    y += 1
    if not is_pulled(x,y+99):
      x += 1
  return x*10000 + y


print(part1())
print(part2())
