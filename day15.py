from intcodecomputer import IntCodeComputer
from queue import Queue, Empty
from utils import defaultdict_to_string
from collections import defaultdict
from threading import Thread
from collections import deque


input_file = 'day15input.txt'

N = 1
S = 2
W = 3
E = 4

BLOCKED = 0
MOVED = 1
FOUND_OXYGEN = 2

oxygen_loc = None

def get_input():
    return [int(x) for x in open(input_file).read().split(',')]


def moves_to(pos, d):
  x, y = pos
  if d == N:
    return x, y-1
  elif d == S:
    return x, y+1
  elif d == W:
    return x-1, y
  elif d == E:
    return x+1, y


def turn_right(facing):
  if facing == N:
    return E
  elif facing == E:
    return S
  elif facing == S:
    return W
  elif facing == W:
    return N


def turn_left(facing):
  if facing == N:
    return W
  elif facing == W:
    return S
  elif facing == S:
    return E
  elif facing == E:
    return N    


def decide_move(pos, facing, m):
  direction = turn_right(facing)
  while m[moves_to(pos, direction)] == '#':
    direction = turn_left(direction)
  
  return direction


def update_position(pos, move, status):
  if status == BLOCKED:
    return pos
  else:
    return moves_to(pos, move)


def update_map(m, pos, move, status):
  dest = moves_to(pos, move)
  if status == BLOCKED:
    m[dest] = '#'
  elif status == FOUND_OXYGEN:
    m[dest] = 'O'
  elif status == MOVED:
    m[dest] = '.'




def get_neighbors(m, pos):
  neighbors = []
  for d in [N, E, S, W]:
    dest = moves_to(pos, d)
    if m[dest] == '.' or m[dest] == 'O':
      neighbors.append(dest)
  return neighbors



def find_path_length(m, start, goal):
  to_explore = deque()
  to_explore.append((start, 0))
  visited = set()
  while len(to_explore) > 0:
    pos, n = to_explore.popleft()
    if pos == goal:
      return n

    visited.add(pos)
    neighbors = get_neighbors(m, pos)
    for neighbor in neighbors:
      if neighbor not in visited:
        to_explore.append((neighbor, n+1))
  return None

def find_oxygen(m):
  for pos in m.keys():
    if m[pos] == 'O':
      return pos

def part1():
  mem = get_input()
  input_q = Queue()
  output_q = Queue()
  comp = IntCodeComputer(mem, input_q, output_q)
  computer_thread = Thread(target=comp.execute)
  computer_thread.start()


  m = defaultdict(lambda: ' ')
  position = (0, 0)
  facing = E
  m[position] = 'D'
  status = None

  i = 0
  while status != FOUND_OXYGEN:
    move = decide_move(position, facing, m)
    input_q.put(move)
    status = output_q.get()
    if status == MOVED:
      facing = move
    new_position = update_position(position, move, status)
    m[position] = '.'
    m[new_position] = 'D'
    update_map(m, position, move, status)
    position = new_position
    i += 1

  return find_path_length(m, (0, 0), find_oxygen(m))


def walls_on_three_sides(m, pos):
  n = 0
  for d in [N, S, E, W]:
    if m[moves_to(pos, d)] == '#':
      n += 1
  return n == 3


def time_to_flood_fill(m):
  pos = find_oxygen(m)
  to_fill = deque()
  to_fill.append((pos, 0))
  filled = set()
  while len(to_fill) > 0:
    pos, n = to_fill.popleft()
    filled.add(pos)
    neighbors = get_neighbors(m, pos)
    for neighbor in neighbors:
      if neighbor not in filled:
        to_fill.append((neighbor, n+1))
  return n

def part2():
  mem = get_input()
  input_q = Queue()
  output_q = Queue()
  comp = IntCodeComputer(mem, input_q, output_q)
  computer_thread = Thread(target=comp.execute)
  computer_thread.start()


  m = defaultdict(lambda: ' ')
  position = (0, 0)
  facing = E
  m[position] = 'D'
  status = None
  visited = set()
  visited.add(position)

  while True:
    move = decide_move(position, facing, m)
    input_q.put(move)
    status = output_q.get()
    if status == MOVED:
      facing = move
    new_position = update_position(position, move, status)
    update_map(m, position, move, status)
    position = new_position
    if position in visited and walls_on_three_sides(m, position):
      break

  return time_to_flood_fill(m)


print(part1())
print(part2())

