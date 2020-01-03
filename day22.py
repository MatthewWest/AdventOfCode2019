from copy import copy
import re
from functools import partial

debug = False

def deal_into_new_stack(deck):
  if debug:
    print('reverse')
  new = copy(deck)
  new.reverse()
  return new


def cut(n, deck):
  if debug:
    print('cut {:}'.format(n))
  return deck[n:] + deck[:n]


def deal_with_increment(n, deck):
  if debug:
    print('deal increment {:}'.format(n))
  new = [None for _ in deck]
  size = len(deck)
  i = 0
  for card in deck:
    new[i] = card
    i = (i + n) % size
  return new


deal_into_new_stack_pattern = re.compile('deal into new stack')
deal_with_increment_pattern = re.compile('deal with increment ([0-9]+)')
cut_pattern = re.compile('cut (-?[0-9]+)')
def parse_input(s):
  operations = []
  
  for line in s.splitlines():
    match = deal_into_new_stack_pattern.match(line)
    if match:
      operations.append(deal_into_new_stack)
      continue
    match = deal_with_increment_pattern.match(line)
    if match:
      n = int(match.group(1))
      operations.append(partial(deal_with_increment, n))
      continue
    match = cut_pattern.match(line)
    if match:
      n = int(match.group(1))
      operations.append(partial(cut, n))
      continue
  return operations


def part1():
  deck = [i for i in range(10007)]
  ops = parse_input(open('day22input.txt').read())
  for op in ops:
    deck = op(deck)
  for i, card in enumerate(deck):
    if card == 2019:
      return i


def reverse_cut(n, deck_length, pos):
  if n < 0:
    n = deck_length - n
  return (pos + n) % deck_length


def reverse_deal_into_new_stack(deck_length, pos):
  return abs(pos - (deck_length-1))


def reverse_deal_with_increment(n, deck_length, pos):
  position_in_round = pos // n
  # could be +1, depending on the alignment
  cards_in_round = deck_length // n
  print('cards_in_round = {:}'.format(cards_in_round))

  if pos % n == 0:
    return pos // n

  offset = pos - n * position_in_round
  offset_per_round = deck_length - cards_in_round * n
  rounds = offset // offset_per_round

  unwrapped_position = rounds * deck_length + pos
  while not (unwrapped_position % deck_length == pos and unwrapped_position % n == 0):
    print('rounds = {:}, unwrapped_position = {:}'.format(rounds, unwrapped_position))
    rounds += 1
    unwrapped_position = rounds * deck_length + pos

  return unwrapped_position // n


def parse_input_to_reverse_tracker(s):
  operations = []
  
  for line in s.splitlines():
    match = deal_into_new_stack_pattern.match(line)
    if match:
      operations.append(reverse_deal_into_new_stack)
      continue
    match = deal_with_increment_pattern.match(line)
    if match:
      n = int(match.group(1))
      operations.append(partial(reverse_deal_with_increment, n))
      continue
    match = cut_pattern.match(line)
    if match:
      n = int(match.group(1))
      operations.append(partial(reverse_cut, n))
      continue
  operations.reverse()
  return operations


s1 = '''deal with increment 7
deal into new stack
deal into new stack'''


reverse_mapping = {}
ops = parse_input_to_reverse_tracker(s1)
cycle_count = 0

def apply_ops(original_pos, deck_length):
  global cycle_count
  if original_pos in reverse_mapping:
    return reverse_mapping[original_pos]
  pos = original_pos
  for op in ops:
    pos = op(deck_length, pos)

  reverse_mapping[original_pos] = pos
  cycle_count += 1
  return pos

prev_cycle_count = None
while prev_cycle_count != cycle_count:
  apply_ops(2020, 119315717514047)
print(cycle_count)
