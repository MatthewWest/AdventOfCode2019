from itertools import combinations
import re
from functools import reduce
import operator
from collections import defaultdict

input_file = 'day12input.txt'
s = open(input_file).read()

s1 = '''<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>'''

s2 = '''<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>'''


class Moon():
  def __init__(self, x, y, z, vx=0, vy=0, vz=0):
    self._x = x
    self._y = y
    self._z = z
    self._vx = vx
    self._vy = vy
    self._vz = vz

  def __key(self):
    return (self._x, self._y, self._z, self._vx, self._vy, self._vz)

  def __hash__(self):
    return hash(self.__key())

  @property
  def x(self):
    return self._x

  @property
  def y(self):
    return self._y

  @property
  def z(self):
    return self._z

  @property
  def vx(self):
    return self._vx
  
  @property
  def vy(self):
    return self._vy

  @property
  def vz(self):
    return self._vz


  def __repr__(self):
    return 'pos=<x={:}, y={:}, z={:}>, vel=<x={:}, y={:}, z={:}>, pot={:}, kin={:}'\
      .format(self.x, self.y, self.z, self._vx, self._vy, self._vz, self.potential_energy(), self.kinetic_energy())
  

  def apply_velocity(self):
    self._x += self._vx
    self._y += self._vy
    self._z += self._vz

  def apply_gravity(self, other):
    if other.x > self.x:
      self._vx += 1
    elif self.x > other.x:
      self._vx -= 1

    if other.y > self.y:
      self._vy += 1
    elif self.y > other.y:
      self._vy -= 1

    if other.z > self.z:
      self._vz += 1
    elif self.z > other.z:
      self._vz -= 1


  def potential_energy(self):
    return abs(self.x) + abs(self.y) + abs(self.z)

  def kinetic_energy(self):
    return abs(self._vx) + abs(self._vy) + abs(self._vz)

  def total_energy(self):
    return self.potential_energy() * self.kinetic_energy()


pattern = re.compile('<x=([-0-9]+), y=([-0-9]+), z=([-0-9]+)>')
def parse_input(s):
  moons = []
  with open(input_file) as f:
    lines = s.splitlines()
    for line in lines:
      match = re.match(pattern, line)
      x = int(match.group(1))
      y = int(match.group(2))
      z = int(match.group(3))
      moons.append(Moon(x, y, z))
  return moons


def time_step(moons):
  for a, b in combinations(moons, 2):
    a.apply_gravity(b)
    b.apply_gravity(a)
  for moon in moons:
    moon.apply_velocity()  


def total_energy(moons):
  total = 0
  for moon in moons:
    total += moon.total_energy()
  return total  


def part1():
  moons = parse_input(s)
  for i in range(1000):
    time_step(moons)

  return total_energy(moons)


def get_x_state(moons):
  xs = [m.x for m in moons]
  vxs = [m.vx for m in moons]
  return tuple(xs + vxs)


def find_xcycle_length(moons):
  x_history = set()
  x_history.add(get_x_state(moons))
  i = 0
  while True:
    time_step(moons)
    i += 1
    x_vals = get_x_state(moons)
    if x_vals in x_history:
      return i
    else:
      x_history.add(get_x_state(moons))


def get_y_state(moons):
  ys = [m.y for m in moons]
  vys = [m.vy for m in moons]
  return tuple(ys + vys)


def find_ycycle_length(moons):
  y_history = set()
  y_history.add(get_y_state(moons))
  i = 0
  while True:
    time_step(moons)
    i += 1
    y_vals = get_y_state(moons)
    if y_vals in y_history:
      return i
    else:
      y_history.add(get_y_state(moons))


def get_z_state(moons):
  zs = [m.z for m in moons]
  vzs = [m.vz for m in moons]
  return tuple(zs + vzs)

def find_zcycle_length(moons):
  z_history = set()
  z_history.add(get_z_state(moons))
  i = 0
  while True:
    time_step(moons)
    i += 1
    z_vals = get_z_state(moons)
    if z_vals in z_history:
      return i
    else:
      z_history.add(get_z_state(moons))      


def prime_factor_counts(n):
  i = 2
  factor_counts = defaultdict(lambda: 0)
  while i*i <= n:
    if n % i:
      if i > 2:
        i += 2
      else:
        i += 1
    else:
      n //= i
      factor_counts[i] += 1
  if n > 1:
    factor_counts[n] += 1
  return factor_counts


def lcm(ns):
  factor_minimum_counts = defaultdict(lambda: 0)
  for length in ns:
    factors = prime_factor_counts(length)
    for factor in factors:
      n_times = factors[factor]
      if n_times > factor_minimum_counts[factor]:
        factor_minimum_counts[factor] = n_times

  p = 1
  for factor in factor_minimum_counts:
    for _ in range(factor_minimum_counts[factor]):
      p *= factor
  return p

def part2():
  moons = parse_input(s)

  xcycle = find_xcycle_length(moons)
  ycycle = find_ycycle_length(moons)
  zcycle = find_zcycle_length(moons)

  return lcm([xcycle, ycycle, zcycle])


print(part1())
print(part2())
