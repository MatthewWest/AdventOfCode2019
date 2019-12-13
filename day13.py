from intcodecomputer import IntCodeComputer
from queue import Queue, Empty
from utils import defaultdict_to_string
from collections import defaultdict
from threading import Thread
from copy import copy
from time import sleep
from os import system

input_file = 'day13input.txt'

def get_input():
    return [int(x) for x in open(input_file).read().split(',')]


def get_tiles(output_q):
  tiles = []
  if output_q.empty():
    raise Empty
  while not output_q.empty():
    x, y, tile = output_q.get(), output_q.get(), output_q.get()
    tiles.append((x, y, tile))
  return tiles


def part1():
  mem = get_input()
  input_q = Queue()
  output_q = Queue()
  comp = IntCodeComputer(mem, input_q, output_q)

  comp.execute()

  tiles = []
  while not output_q.empty():
    x, y, tile = output_q.get(), output_q.get(), output_q.get()
    tiles.append((x, y, tile))

  blocks = 0
  for x, y, tile in tiles:
    if tile == 2:
      blocks += 1

  print(blocks)


EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4
class Game():
  def __init__(self, mem, in_q, out_q):
    self._in_q = in_q
    self._out_q = out_q
    self._comp = IntCodeComputer(mem, in_q, out_q)
    self._state = defaultdict(lambda: EMPTY)
    self._prev_ball = None
    self._ball = None
    self._paddle = None
    self._score = None

    tiles = self.run_tick()

  def __repr__(self):
    to_print = copy(self._state)
    to_print[self._ball] = BALL
    to_print[self._paddle] = PADDLE
    print('High Score: {:}'.format(self._score))
    return defaultdict_to_string(to_print,
      {
        EMPTY: ' ',
        WALL: '#',
        BLOCK: '@',
        PADDLE: '—',
        BALL: 'O'
      })

  @property
  def halted(self):
    return self._comp.halted

  @property
  def ball(self):
    return self._ball

  @property
  def prev_ball(self):
    return self._prev_ball

  @property
  def paddle(self):
    return self._paddle
  
  

  def update_state(self, tiles):
    for x, y, tile in tiles:
      if x == -1 and y == 0:
        self._score = tile
        continue
      elif tile == BALL:
        self._prev_ball = self._ball
        self._ball = (x, y)
      elif tile == PADDLE:
        self._paddle = (x, y)
      else:
        self._state[(x,y)] = tile

  def run_tick(self, joystick_in=0):
    self._in_q.put(joystick_in)

    try:
      self._comp.execute(blocking=False)
    except Empty:
      pass
    # print('halted = {:}'.format(self._comp.halted))
    tiles = get_tiles(self._out_q) 
    self.update_state(tiles)


def set_up_game():

  mem = get_input()
  mem[0] = 2
  input_q = Queue()
  output_q = Queue()

  game = Game(mem, input_q, output_q)
  return game


def choose_move(game):
  paddle_x = game.paddle[0]
  ball_x = game.ball[0]
  if ball_x > paddle_x:
    return 1
  elif ball_x < paddle_x:
    return -1

  return 0

def part2():
  game = set_up_game()
  print(game)
  while not game.halted:
    game.run_tick(joystick_in=choose_move(game))
    print(game, flush=True)
    sleep(0.01)

  print(game, flush=True)




