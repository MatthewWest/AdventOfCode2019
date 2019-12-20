from collections import defaultdict
from utils import defaultdict_repr, find_coordinate_bounds
from collections import deque
import re
from copy import copy


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


def resolve_all_wall_deps_to_keys(all_deps):
  all_new_deps = {}
  for k in all_deps:
    if all_deps.get(k) is None:
      all_new_deps[k] = None
      continue
    deps = set(all_deps.get(k))
    new_deps = set()    
    while True:
      for dep in deps:
        if is_key(dep):
          new_deps.add(dep)
        else:
          new_deps.update(all_deps.get(dep))
      if new_deps == deps:
        break
      deps = copy(new_deps)
    all_new_deps[k] = [k for k in new_deps if is_key(k)]
  all_new_deps = {k: all_new_deps[k] for k in all_new_deps if is_key(k)} 
  return all_new_deps


def find_dependencies(m, pos):
  visited = set()
  to_visit = deque()
  to_visit.append((pos, None))  # coordinate + the immediate blocking dependency
  blocked_by = defaultdict(lambda: [])
  while to_visit:
    p, blockers = to_visit.popleft()
    c = m[p]
    if is_key(c):
      if blockers:
        for blocker in blockers:
          blocked_by[c].append(blocker)
      else:
        blocked_by[c] = None
    elif is_door(c):
      blocked_by[c].append(c.lower())
      if blockers:
        for blocker in blockers:
          blocked_by[c].append(blocker)
      blockers = [c]
    for n in get_neighbors(m, p):
      if n not in visited:
        to_visit.append((n, blockers))
    visited.add(p)

  return resolve_all_wall_deps_to_keys(blocked_by)


def makes_available(dependencies):
  is_depended_on = defaultdict(lambda: [])
  for c in dependencies:
    deps = dependencies[c]
    if deps is None:
      continue
    for dep in deps:
      is_depended_on[dep].append(c)
  return is_depended_on


def find_keys(m):
  locs = {}
  min_x, max_x, min_y, max_y = find_coordinate_bounds(m)
  for x in range(min_x, max_x+1):
    for y in range(min_y, max_y+1):
      c = m[(x, y)]
      if is_key(c):
        locs[c] = (x,y)
  return locs


def find_path_not_crossing_other_key(m, start, dest):
  visited = set()
  to_visit = deque()
  to_visit.append(start)
  paths = {start: []}
  keys_needed = defaultdict(lambda: set())
  while to_visit:
    p = to_visit.popleft()
    if p == dest:
      return paths[p], keys_needed[p]
    c = m[p]
    # if is_key(c) and p != start and p != dest:
    #   continue
    if is_door(c):
      keys_needed[p].add(c.lower())
    for n in get_neighbors(m, p):
      if n not in visited:
        to_visit.append(n)
        paths[n] = paths[p] + [n]
        keys_needed[n] = copy(keys_needed[p])
    visited.add(p)

  if dest in paths:
    return paths[dest], keys_needed[dest]
  else:
    return None, None


def find_initial_candidates(deps):
  candidates = []
  for c in deps:
    if deps[c] is None:
      candidates.append(c)
  return candidates


def find_all_paths(m, pos):
  keys = find_keys(m)
  paths = defaultdict(lambda: {})
  deps = defaultdict(lambda: {})
  for k in keys:
    p, needed = find_path_not_crossing_other_key(m, pos, keys[k])
    if p is not None and needed is not None:
      paths['@'][k], deps['@'][k] = p, needed
  for a in keys:
    for b in keys:
      if b == a:
        continue
      p, needed = find_path_not_crossing_other_key(m, keys[a], keys[b])
      if p is not None and needed is not None:
        paths[a][b], deps[a][b] = p, needed
  return paths, deps


def get_candidates(start, available, deps):
  candidates = []
  for dest in deps[start]:

    if deps[start][dest] <= available:
      candidates.append(dest)
  return candidates


def find_shortest_path_to_all_keys(m, start):
  locs = find_locs(m)
  deps = find_dependencies(m, start)
  candidates = set(find_initial_candidates(deps))
  reverse_deps = makes_available(deps)
  return find_shortest_path(m, start, candidates, set(), locs, deps, reverse_deps)


def find_shortest_path(m, 
                       start, 
                       candidates,
                       can_open,
                       locs,
                       deps,
                       downstreams):
  # Base case, if we have no more keys to find, return
  if len(candidates) == 0:
    return []

  shortest_path = None
  shortest_length = float('inf')
  for candidate in candidates:
    path = find_path(m, start, locs[candidate], can_open)
    if path is None:
      continue

    now_can_open = copy(can_open)
    now_can_open.add(candidate.upper())

    new_candidates = set()
    for c in candidates | set(downstreams[candidate]):
      if c == candidate:
        continue
      new_candidates.add(c)

    rest = find_shortest_path(m,
      locs[candidate],
      new_candidates,
      now_can_open,
      locs,
      deps,
      downstreams)

    path = path + rest
    if len(path) < shortest_length:
      shortest_path = path
      shortest_length = len(path)
  return shortest_path


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

m, pos = parse_input(s4)
# m, pos = get_input()

paths, deps = find_all_paths(m, pos)
keys = find_keys(m).keys()
visited = set()
available = set()
at = '@'
candidates = get_candidates(at, available, deps)

def find_shortest_path_to_all_keys(m, at, candidates, available):
  # print(at, candidates, available)
  s_len = float('inf')
  s_path = None
  for candidate in candidates:
    if candidate in available:
      continue

    now_available = available | set([candidate])
    path = paths[at][candidate]
    rest = find_shortest_path_to_all_keys(m,
      candidate,
      get_candidates(candidate, now_available, deps),
      now_available)
    path = path + rest
    if len(path) < s_len:
      s_len = len(path)
      s_path = path
  if s_path is None:
    return []
  else:
    return s_path


path = find_shortest_path_to_all_keys(m, '@', candidates, set())
print(len(path))
