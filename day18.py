from collections import defaultdict
from utils import defaultdict_repr, find_coordinate_bounds
from collections import deque
import re
from copy import copy
from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any


def parse_input(s):
  m = defaultdict(lambda: '#')
  for y, line in enumerate(s.splitlines()):
    for x, c in enumerate(line):
      if c == '@':
        pos = (x, y)
        c = '.'
      m[(x, y)] = c
  return m, pos


def get_input():
  return parse_input(open('day18input.txt').read())


def get_neighbors(m, pos):
  x, y = pos
  neighbors = []
  for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
    cand = (x+dx, y+dy)
    if m[cand] != '#':
      neighbors.append(cand)
  return neighbors


key_pattern = re.compile('[a-z]')
def is_key(c):
  return bool(key_pattern.match(c))


door_pattern = re.compile('[A-Z]')
def is_door(c):
  return bool(door_pattern.match(c))


def print_map(m, pos):
  m = copy(m)
  m[pos] = '@'
  print(defaultdict_repr(m))


def find_path(m, start, dest):
  visited = set()
  to_visit = deque()
  to_visit.append(start)
  paths = {start: []}
  needed_keys = defaultdict(lambda: set())
  while to_visit:
    p = to_visit.popleft()
    visited.add(p)    
    c = m[p]
    if is_door(c):
      needed_keys[p].add(c.lower())
    for n in get_neighbors(m, p):
      if n not in visited:
        to_visit.append(n)
        paths[n] = paths[p] + [n]
        needed_keys[n] = copy(needed_keys[p])

  if dest in paths:
    return paths[dest], needed_keys[dest]
  else:
    return None, None


def find_points_of_interest(m):
  locs = set()
  min_x, max_x, min_y, max_y = find_coordinate_bounds(m)
  for x in range(min_x, max_x+1):
    for y in range(min_y, max_y+1):
      if is_key(m[(x, y)]):
        locs.add((x,y))
  return locs

def find_paths_and_needed_keys(m, start):
  locs = list(find_points_of_interest(m)) + [start]
  paths = defaultdict(lambda: {})
  for a in locs:
    for b in locs:
      # Don't navigate to ourselves or to the start or anywhere to start
      if a is b or b is start:
        continue
      path, keys_needed = find_path(m, a, b)
      paths[a][b] = (path, keys_needed)
  return paths


class Node:
  def __init__(self, loc, keys):
    self._loc = loc
    self._keys = frozenset(list(keys))

  @property
  def loc(self):
    return self._loc

  @property
  def keys(self):
    return self._keys
  
  def __key(self):
    return (self._loc, self._keys)

  def __hash__(self):
    return hash(self.__key())

  def __eq__(self, other):
    return self.__key() == other.__key()

  def __lt__(self, other):
    return self.keys < other.keys

  def __repr__(self):
    return 'Node<loc={:}, keys={:}>'.format(self._loc, set(self._keys))


def find_node_neighbors(m, node, paths):
  pos, keys = node.loc, node.keys
  visited = set()
  to_visit = deque()
  paths_from_pos = paths[pos]
  node_neighbors = []
  for dest in paths_from_pos:
    if m[dest] in keys:
      continue
    path, keys_needed = paths_from_pos[dest]
    if keys_needed <= keys:
      node_neighbors.append((len(path), Node(dest, list(keys) + [m[dest]])))
  return node_neighbors


from heapq import heapify, heappush, heappop

class PriorityDict(dict):
  """Dictionary that can be used as a priority queue.

  Keys of the dictionary are items to be put into the queue, and values
  are their respective priorities. All dictionary methods work as expected.
  The advantage over a standard heapq-based priority queue is
  that priorities of items can be efficiently updated (amortized O(1))
  using code as 'thedict[item] = new_priority.'

  The 'smallest' method can be used to return the object with lowest
  priority, and 'pop_smallest' also removes it.

  The 'sorted_iter' method provides a destructive sorted iterator.
  """
  
  def __init__(self, *args, **kwargs):
    super(PriorityDict, self).__init__(*args, **kwargs)
    self._rebuild_heap()

  def _rebuild_heap(self):
    self._heap = [(v, k) for k, v in self.items()]
    heapify(self._heap)

  def smallest(self):
    """Return the item with the lowest priority.

    Raises IndexError if the object is empty.
    """
    
    heap = self._heap
    v, k = heap[0]
    while k not in self or self[k] != v:
      heappop(heap)
      v, k = heap[0]
    return k

  def pop_smallest(self):
    """Return the item with the lowest priority and remove it.

    Raises IndexError if the object is empty.
    """
    
    heap = self._heap
    v, k = heappop(heap)
    while k not in self or self[k] != v:
      v, k = heappop(heap)
    del self[k]
    return k

  def __setitem__(self, key, val):
    # We are not going to remove the previous value from the heap,
    # since this would have a cost O(n).
    
    super(PriorityDict, self).__setitem__(key, val)
    
    if len(self._heap) < 2 * len(self):
      heappush(self._heap, (val, key))
    else:
      # When the heap grows larger than 2 * len(self), we rebuild it
      # from scratch to avoid wasting too much memory.
      self._rebuild_heap()

  def setdefault(self, key, val):
    if key not in self:
      self[key] = val
      return val
    return self[key]

  def update(self, *args, **kwargs):
    # Reimplementing dict.update is tricky -- see e.g.
    # http://mail.python.org/pipermail/python-ideas/2007-May/000744.html
    # We just rebuild the heap from scratch after passing to super.
    
    super(PriorityDict, self).update(*args, **kwargs)
    self._rebuild_heap()

  def sorted_iter(self):
    """Sorted iterator of the priority dictionary items.

    Beware: this will destroy elements as they are returned.
    """
    while self:
      yield self.pop_smallest()

def djikstra(m, pos, paths):
  pq = PriorityDict()
  dist = defaultdict(lambda: float('inf'))
  prev = {}
  start = Node(pos, [])
  # Start with the current position and an empty set of keys at distance 0
  pq[start] = 0
  dist[start] = 0
  while pq:
    node = pq.pop_smallest()
    for length_to_neighbor, neighbor in find_node_neighbors(m, node, paths):
      alt_dist = dist[node] + length_to_neighbor
      if alt_dist < dist[neighbor]:
        dist[neighbor] = alt_dist
        prev[neighbor] = node
        pq[neighbor] = alt_dist
  return dist, prev



s1 = '''#########
#b.A.@.a#
#########'''

s2 = '''########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################'''

s3 = '''########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################'''


s4 = '''#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################'''

s5 = '''########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################'''


def part1():
  m, pos = get_input()

  paths = find_paths_and_needed_keys(m, pos)
  dist, prev = djikstra(m, pos, paths)

  key_count = 0
  end = None
  for node in dist:
    if len(node.keys) > key_count:
      key_count = len(node.keys)

  least_distance = float('inf')
  for node in dist:
    if len(node.keys) != key_count:
      continue
    if dist[node] < least_distance:
      least_distance = dist[node]

  return least_distance


class Node2:
  def __init__(self, robot_locs, keys):
    self._locs = frozenset(list(robot_locs))
    self._keys = frozenset(list(keys))

  @property
  def locs(self):
    return self._locs

  @property
  def keys(self):
    return self._keys
  
  def __key(self):
    return (self._locs, self._keys)

  def __hash__(self):
    return hash(self.__key())

  def __eq__(self, other):
    return self.__key() == other.__key()

  def __lt__(self, other):
    return self.keys < other.keys

  def __repr__(self):
    return 'Node<locs={:}, keys={:}>'.format(self.locs, set(self.keys))



def correct_map_and_get_locs(m, pos):
  x, y = pos
  m[(x, y)] = '#'
  m[(x-1, y)] = '#'
  m[(x+1, y)] = '#'
  m[(x, y-1)] = '#'
  m[(x, y+1)] = '#'
  locs = [(x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)]
  return locs


def find_node_neighbors2(m, node, paths):
  locs, keys = node.locs, node.keys
  visited = set()
  node_neighbors = []  
  for loc in locs:
    for dest in paths[loc]:
      if m[dest] in keys:
        continue
      path, keys_needed = paths[loc][dest]
      if not path:  # no path
        raise Exception
      if keys_needed <= keys:
        new_locs = set(locs)
        new_locs.remove(loc)
        new_locs.add(dest)
        node_neighbors.append((len(path), Node2(new_locs, list(keys) + [m[dest]])))
  return node_neighbors


def djikstra2(m, locs, paths):
  pq = PriorityDict()
  steps = defaultdict(lambda: float('inf'))
  prev = {}
  start = Node2(locs, [])
  # Start with the current positions and an empty set of keys at distance 0
  pq[start] = 0
  steps[start] = 0
  while pq:
    node = pq.pop_smallest()
    for length_to_neighbor, neighbor in find_node_neighbors2(m, node, paths):
      alt_steps = steps[node] + length_to_neighbor
      if alt_steps < steps[neighbor]:
        steps[neighbor] = alt_steps
        prev[neighbor] = node
        pq[neighbor] = alt_steps
  return steps, prev

def find_paths_and_needed_keys2(m, locs):
  locs = set(locs)
  to_find = list(find_points_of_interest(m)) + list(locs)
  paths = defaultdict(lambda: {})
  for a in to_find:
    for b in to_find:
      # Don't navigate to ourselves or to the start or anywhere to start
      if a is b or b in locs:
        continue
      path, keys_needed = find_path(m, a, b)
      if path:
        paths[a][b] = (path, keys_needed)
  return paths


def part2():
  m, pos = get_input()
  locs = correct_map_and_get_locs(m, pos)

  paths = find_paths_and_needed_keys2(m, locs)
  dist, prev = djikstra2(m, locs, paths)

  key_count = 0
  end = None
  for node in dist:
    if len(node.keys) > key_count:
      key_count = len(node.keys)

  least_distance = float('inf')
  for node in dist:
    if len(node.keys) != key_count:
      continue
    if dist[node] < least_distance:
      least_distance = dist[node]

  return least_distance


print(part1())
print(part2())
