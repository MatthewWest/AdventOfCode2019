from itertools import cycle
import numpy as np

base_pattern = [0, 1, 0, -1]

# O(1)
def make_pattern(pos):
  pattern = []
  for n in base_pattern:
    pattern += [n] * pos
  pattern = pattern[1:] + [pattern[0]]
  return cycle(pattern)


# O(n)
def apply_pattern(nums, pattern):
  n = 0
  for num, multiplier in zip(nums, pattern):
    # print('{:}*{:}'.format(num, multiplier))
    n += num * multiplier
  return abs(n) % 10


# O(n^2)
def do_phase(nums):
  new_nums = []
  for pos in range(len(nums)):
    pattern = make_pattern(pos + 1)  # 1-indexed
    new_nums.append(apply_pattern(nums, pattern))
  return new_nums


# O(n^2 * 100)
def do_n_phases(nums, n):
  for i in range(n):
    nums = do_phase(nums)
    # print("phase {:} done".format(i))
  return nums


def make_integer(nums):
  n = 0
  for i in nums:
    n *= 10
    n += i
  return n



def part1():
  s = open('day16input.txt').read().strip()
  nums = [int(c) for c in s]
  result = do_n_phases(nums, 100)
  return make_integer(result[:8])


def do_second_half_phase(nums):
  for i in range(len(nums)-2, -1, -1):
    nums[i] = (nums[i] + nums[i+1]) % 10


def part2():
  s = open('day16input.txt').read().strip()
  nums = [int(c) for c in s] * 10000
  offset = make_integer(nums[:7])
  nums = nums[offset:]
  for i in range(100):
    do_second_half_phase(nums)
  return make_integer(nums[:8])

print(part1())
print(part2())

# There must be some trick with cancelling out - you'll get to a point where any further inputs will
# just cancel

# As is the algorithm is O(n^2)


