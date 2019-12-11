from intcodecomputer import IntCodeComputer
from queue import Queue
from threading import Thread
from collections import defaultdict
from utils import defaultdict_to_string

input_file = 'day11input.txt'


def get_input():
    return [int(x) for x in open(input_file).read().split(',')]


def move(pos, d):
  if d == 'N':
    return pos[0], pos[1] - 1
  elif d == 'S':
    return pos[0], pos[1] + 1
  elif d == 'E':
    return pos[0] + 1, pos[1]
  elif d == 'W':
    return pos[0] - 1, pos[1]

def rotate(d, val):
  dirs = ['N', 'E', 'S', 'W']
  if val == 0:
    cur = dirs.index(d)
    new = cur - 1
    if new < 0:
      new = len(dirs) - 1
  elif val == 1:
    cur = dirs.index(d)
    new = (cur + 1) % len(dirs)
  return dirs[new]

def part1():
  pos = (49, 49)
  direc = 'N'
  panel_is_painted = defaultdict(lambda: False)
  panel_color = defaultdict(lambda: 'b')
  

  input_queue = Queue()
  output_queue = Queue()

  computer = IntCodeComputer(get_input(), input_queue, output_queue)

  computer_thread = Thread(target=computer.execute)

  computer_thread.start()

  while not computer.halted:
    if panel_color[pos] == 'w':
      val = 1
    else:
      val = 0
    input_queue.put(val)
    color = output_queue.get()
    turn = output_queue.get()
    if color == 0:
      panel_is_painted[pos] = True
      panel_color[pos] = 'b'
    elif color == 1:
      panel_is_painted[pos] = True
      panel_color[pos] = 'w'

    direc = rotate(direc, turn)
    pos = move(pos, direc)

  return len(panel_is_painted)


def part2():
  pos = (0, 0)
  direc = 'N'
  panel_is_painted = defaultdict(lambda: False)
  panel_color = defaultdict(lambda: 'b')
  panel_color[pos] = 'w'
  
  input_queue = Queue()
  output_queue = Queue()

  computer = IntCodeComputer(get_input(), input_queue, output_queue)

  computer_thread = Thread(target=computer.execute)

  computer_thread.start()

  while not computer.halted:
    if panel_color[pos] == 'w':
      val = 1
    else:
      val = 0
    input_queue.put(val)
    color = output_queue.get()
    turn = output_queue.get()
    if color == 0:
      panel_is_painted[pos] = True
      panel_color[pos] = 'b'
    elif color == 1:
      panel_is_painted[pos] = True
      panel_color[pos] = 'w'

    direc = rotate(direc, turn)
    pos = move(pos, direc)

  return defaultdict_to_string(panel_color, {'b': ' ', 'w': '#'})


print(part1())
print(part2())
