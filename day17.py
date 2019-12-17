from intcodecomputer import IntCodeComputer
from queue import Queue, Empty
from utils import defaultdict_to_string
from collections import defaultdict
from collections import deque
from threading import Thread
from copy import copy

input_file = 'day17input.txt'

directions = {
  'N': (0, -1),
  'S': (0, 1),
  'W': (-1, 0),
  'E': (1, 0),
}

def get_input():
    return [int(x) for x in open(input_file).read().split(',')]


def get_map():
  mem = get_input()
  input_q = Queue()
  output_q = Queue()
  comp = IntCodeComputer(mem, input_q, output_q)
  comp.execute()  
  cs = []
  while not output_q.empty():
    cs.append(chr(output_q.get()))
  s = ''.join(cs)

  m = defaultdict(lambda: '.')
  for y, line in enumerate(s.splitlines()):
    for x, c in enumerate(line):
      if c != '.' and c != '#':
        pos = (x, y)
        if c == '^':
          facing = 'N'
        elif c == 'v':
          facing = 'S'
        elif c == '<':
          facing = 'W'
        elif c == '>':
          facing = 'E'
        else:
          raise Exception("Invalid character {:}".format(c))
        c = '#'
      m[(x, y)] = c

  return m, pos, facing


def get_scaffolding_set(m):
  on_scaffolding = set()
  for (x, y) in m:
    if m.get((x, y)) == '#':
      on_scaffolding.add((x, y))
  return on_scaffolding


def get_intersections(m):
  intersections = set()
  for x, y in m:
    if m.get((x, y)) != '#':
      continue
    c = 0
    for dx, dy in directions.values():
      if m.get((x+dx, y+dy)) == '#':
        c += 1
    if c == 4:
      intersections.add((x, y))
  return intersections

def part1():
  m, pos, facing = get_map()

  on_scaffolding = get_scaffolding_set(m)
  intersections = get_intersections(m)

  n = 0
  for x, y in intersections:
    n += x*y

  return n


def get_neighbors(pos):
  x, y = pos
  neighbors = []
  directions = [(0, 1), (1, 0), (-1, 0), (1, 0)]  
  for dx, dy in directions:
    neighbors.append((x+dx, y+dy))
  return neighbors


def find_next_direction(m, pos, to_visit):
  x, y = pos
  for d in directions:
    dx, dy = directions[d]
    if (x+dx, y+dy) in to_visit:
      return d


def map_to_string(m, pos):
  m = copy(m)
  m[pos] = '^'
  return defaultdict_to_string(m, {'.': '.', '^': '^', '#': '#'})


def find_turn(prev_dir, new_dir):
  directions = ['N', 'E', 'S', 'W']
  prev_i = directions.index(prev_dir)
  new_i = directions.index(new_dir)
  if (prev_i + 1) % 4 == new_i:
    return 'R'
  elif (new_i + 1) % 4 == prev_i:
    return 'L'
  else:
    print('prev_dir: {:}, new_dir: {:}'.format(prev_dir, new_dir))
    raise Exception


def plan_path(m, pos, facing):
  to_visit = get_scaffolding_set(m)
  intersections = get_intersections(m)
  path = []
  go_forward_dist = 0
  while to_visit:
    x, y = pos
    dx, dy = directions[facing]
    if (x+dx, y+dy) not in to_visit:
      if go_forward_dist > 0:
        path.append(str(go_forward_dist))
        go_forward_dist = 0
      facing_prev = facing
      facing = find_next_direction(m, pos, to_visit)
      if facing is None:
        break
      path.append(find_turn(facing_prev, facing))

      dx, dy = directions[facing]
    if pos in intersections:
      intersections.remove(pos)
    elif pos in to_visit:
      to_visit.remove(pos)
    pos = x+dx, y+dy
    go_forward_dist += 1
  return path


def lcs(a, b):
  m = len(a)
  n = len(b)

  l = 0
  row, col = 0, 0 
  LongestCommonSuffix = [[None]*(n+1) for i in range(m+1)]
  for i in range(m+1):
    for j in range(n+1):
      if i == 0 or j == 0:
        LongestCommonSuffix[i][j] = 0
      elif a[i-1] == b[j-1]:
        LongestCommonSuffix[i][j] = LongestCommonSuffix[i-1][j-1] + 1
        if LongestCommonSuffix[i][j] > l:
          l = LongestCommonSuffix[i][j]
          row = i
          col = j
      else:
        LongestCommonSuffix[i][j] = 0

  if l == 0:
    return [], 0
  result = ['0'] * l
  longest = l

  l -= 1
  while LongestCommonSuffix[row][col] != 0:
    result[l] = a[row-1]
    l -= 1
    row -= 1
    col -= 1
  return result, longest


def moves_covered_if_used(path, seq, unusable=set()):
  n = 0
  for i in range(len(path)):
    matches = True
    for a, b in zip(path[i:], seq):
      if a != b or a in unusable:
        matches = False
        break
    if matches:
      n += len(seq)
  return n


def find_starting_index(path, seq):
  if len(seq) > len(path):
    return None
  for i in range(len(path)):
    matches = True
    for a, b in zip(path[i:], seq):
      if a != b:
        matches = False
        break
    if matches:
      return i
  return None


def sequence_occurs_at_least_twice(path, seq):
  for i in range(len(path)):
    a = path[:i]
    b = path[i:]
    if find_starting_index(a, seq) and find_starting_index(b, seq):
      return True
  return False


def sequence_covering_most_moves(path, unusable=set()):
  max_mvs = 0
  max_seq = []
  for i in range(len(path)):
    for j in range(i, len(path)):
      seq = path[i:j]
      if not sequence_occurs_at_least_twice(path, seq):
        continue
      moves_covered = moves_covered_if_used(path, seq, unusable)
      if moves_covered > max_mvs:
        max_mvs = moves_covered
        max_seq = seq
  return max_seq


def replace_seq_with_function(path, seq, func):
  ind = find_starting_index(path, seq)
  while ind:
    path[ind:ind+len(seq)] = [func]
    ind = find_starting_index(path, seq)
  return path


def print_line(output_q):
  output = []
  while True:
    c = output_q.get()
    if c == ord('\n'):
      break
    else:
      output.append(chr(c))
  print(''.join(output))


def insert_line(input_q, line):
  print('>{:}'.format(line))
  if line[-1] != '\n':
    line = line + '\n'
  for c in line:
    input_q.put(ord(c))


def run_until_blocks(comp):
  try:
    comp.execute(blocking=False)
  except Exception:
    pass


def part2():
  m, pos, facing = get_map()
  path = plan_path(m, pos, facing)

  # This part I massaged by hand after finding the path by program
  A = ['L', '10', 'R', '8', 'R', '6', 'R', '10',]
  B = ['L', '12', 'R', '8', 'L', '12',]
  C = ['L', '10', 'R', '8', 'R', '8']
  routine = ['A', 'B', 'A', 'B', 'C', 'C', 'B', 'A', 'C', 'A']

  mem = get_input()
  mem[0] = 2
  input_q = Queue()
  output_q = Queue()
  comp = IntCodeComputer(mem, input_q, output_q)

  run_until_blocks(comp)
  while not output_q.empty():
    print_line(output_q)
  insert_line(input_q, ','.join(routine))
  run_until_blocks(comp)  
  print_line(output_q)
  insert_line(input_q, ','.join(A))
  run_until_blocks(comp)  
  print_line(output_q)
  insert_line(input_q, ','.join(B))
  run_until_blocks(comp)  
  print_line(output_q)
  insert_line(input_q, ','.join(C))
  run_until_blocks(comp)  
  print_line(output_q)
  insert_line(input_q, 'n')
  run_until_blocks(comp)  

  output = []
  dust_collected = None
  while not output_q.empty():
    c = output_q.get()
    if c <= 255:
      output.append(chr(c))
    else:
      dust_collected = c
  print(''.join(output))
  return dust_collected

print(part2())
