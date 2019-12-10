import math

def gcd(a, b):
  while b:
    a, b = b, a % b
  return a

def can_see(a, b, field):
  xa, ya = a
  xb, yb = b

  rise = yb - ya
  run = xb - xa

  if run == 0:
    if rise < 0:
      step = -1
    else:
      step = 1
    ys = range(ya, yb, step)
    xs = [xa] * len(ys)
  elif rise == 0:
    if run > 0:
      step = 1
    else:
      step = -1
    xs = range(xa, xb, step)
    ys = [ya] * len(xs)
  else:
    if abs(rise) == abs(run):
      gcd_slope = abs(rise)
    else:
      # find the smallest integer rise and run. We need to jump by this many
      gcd_slope = abs(gcd(rise, run))
    xstep = run // gcd_slope
    ystep = rise // gcd_slope
    if run < 0 and xstep > 0:
      xstep *= -1
    if rise < 0 and ystep > 0:
      ystep *= -1
    xs = range(xa, xb, xstep)
    ys = range(ya, yb, ystep)

  for x, y in zip(xs, ys):
    if x == xa and y == ya:
      continue
    if field[y][x] == '#':
      return False
  return True

def parse_input(s):
  s_lines = s.splitlines()
  field = []
  for s_line in s_lines:
    line = []
    for c in s_line:
      line.append(c)
    field.append(line)
  return field


def find_asteroids(field):
  asteroids = set()
  for x in range(len(field)):
    for y in range(len(field)):
      if field[y][x] == '#':
        asteroids.add((x, y))
  return asteroids

s1 = '''.#..#
.....
#####
....#
...##'''

s2 = '''......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####'''

s3 = '''#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.'''

s4 = '''.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..'''

s5 = '''.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##'''

def count_visible(asteroid, asteroids, field):
  count = 0
  for a in asteroids:
    if asteroid == a:
      continue
    if can_see(asteroid, a, field):
      count += 1
  return count


def get_input_field():
  s = open('day10input.txt').read()
  return parse_input(s)


def find_best_station_location(field, asteroids):
  asteroids = find_asteroids(field)
  can_see_counts = {}

  for candidate in asteroids:
    can_see_counts[candidate] = count_visible(candidate, asteroids, field)

  max_visible = 0
  best_candidate = None
  for candidate in can_see_counts:
    count = can_see_counts[candidate]
    if count > max_visible:
      best_candidate = candidate
      max_visible = count

  return max_visible, best_candidate


def part1():
  field = get_input_field()
  asteroids = find_asteroids(field)
  return find_best_station_location(field, asteroids)[0]


def find_angle_in_degrees(a, b):
  rads = math.atan2(-(b[1] - a[1]), b[0] - a[0])
  degs = math.degrees(rads)
  return degs


def find_first_index_gt_or_eq(l, val):
  a, b = 0, len(l)-1
  while a < b:
    mid = (a + b) // 2
    if l[mid] < val:
      a = mid
    elif l[mid] > val:
      b = mid
    elif l[mid] == val:
      i = mid
      while l[i] == val:
        i -= 1
      return i + 1
  i = a - 5
  while l[i] < val:
    i += 1
  return i


def part2():
  field = get_input_field()
  asteroids = find_asteroids(field)
  _, station = find_best_station_location(field, asteroids)

  angle_to_asteroid = {}
  for asteroid in asteroids:
    if asteroid == station:
      continue
    angle = find_angle_in_degrees(station, asteroid)
    if angle in angle_to_asteroid:
      angle_to_asteroid[angle].append(asteroid)
    else:
      angle_to_asteroid[angle] = [asteroid]

  sorted_angles = list(angle_to_asteroid.keys())
  sorted_angles.sort()

  vaporized = 0
  i = find_first_index_gt_or_eq(sorted_angles, 90)
  n_angles = len(sorted_angles)
  while len(asteroids) > 1:
    angle = sorted_angles[i]
    path = angle_to_asteroid[angle]
    for target in path:
      if target in asteroids and can_see(station, target, field):
        field[target[1]][target[0]] = '.'
        vaporized += 1
        asteroids.remove(target)

        if vaporized == 200:
          return target[0] * 100 + target[1]
        break
    if i == 0:
      i = n_angles - 1
    else:
      i -= 1

print(part1())
print(part2())
