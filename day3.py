import re
import math

input_string = open('day3input.txt').read()
# input_string = 'R8,U5,L5,D3,\nU7,R6,D4,L4,'

wires = input_string.split('\n')
wire1 = [s for s in wires[0].split(',') if s != '']
wire2 = [s for s in wires[1].split(',') if s != '']

def move(pos, direction):
    if direction == 'R':
        return pos[0] + 1, pos[1]
    elif direction == 'L':
        return pos[0] - 1, pos[1]
    elif direction == 'U':
        return pos[0], pos[1] + 1
    elif direction ==  'D':
        return pos[0], pos[1] - 1


segment_regex = re.compile('([RULD])([0-9]+)')
def get_occupied_points(wire):
    points = set()
    pos = (0, 0)
    for segment in wire:
        match = segment_regex.match(segment)
        direction, distance = match.group(1), int(match.group(2))
        for i in range(1, distance+1):
            pos = move(pos, direction)
            points.add(pos)
    return points

def get_wire_points_with_distance(wire):
    points = {}
    pos = (0, 0)
    length = 0
    for segment in wire:
        match = segment_regex.match(segment)
        direction, distance = match.group(1), int(match.group(2))
        for i in range(1, distance+1):
            pos = move(pos, direction)
            length += 1
            if not pos in points:
                points[pos] = length
    return points

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])



def part1():
    intersections = get_occupied_points(wire1) & get_occupied_points(wire2)
    closest = None
    closest_distance = float("inf")
    for pos in intersections:
        dist = manhattan_distance((0, 0), pos)
        if dist < closest_distance:
            closest_distance = dist
            closest = pos
            print(pos, dist)


    return closest_distance

def part2():
    wire1_distances = get_wire_points_with_distance(wire1)
    wire2_distances = get_wire_points_with_distance(wire2)
    intersections = set(wire1_distances.keys()) & set(wire2_distances.keys())

    closest = None
    closest_distance = float("inf")
    for pos in intersections:
        dist = wire1_distances[pos] + wire2_distances[pos]
        if dist < closest_distance:
            closest_distance = dist
            closest = pos
    return closest_distance

print(part1())
print(part2())

