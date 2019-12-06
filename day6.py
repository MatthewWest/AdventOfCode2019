import re
from collections import deque

strings = open('day6input.txt').read().splitlines()

regex = re.compile('([A-Z0-9]+)\)([A-Z0-9]+)')
def parse(s):
	match = regex.match(s)
	return match.group(1), match.group(2)

def part1():
	orbits = {}
	planets = set()
	for s in strings:
		inner, outer = parse(s)
		orbits[outer] = inner
		planets.add(inner)
		planets.add(outer)

	planets.remove('COM')

	n = 0
	for planet in planets:
		p = planet
		while True:
			p = orbits[p]
			n += 1
			if p == 'COM':
				break
	return n

def add_to_graph(dict, a, b):
	if a in dict:
		dict[a].append(b)
	else:
		dict[a] = [b]
	if b in dict:
		dict[b].append(a)
	else:
		dict[b] = [a]

def part2():
	edges = {}
	planets = set()
	for s in strings:
		inner, outer =parse(s)
		add_to_graph(edges, inner, outer)
		planets.add(inner)
		planets.add(outer)
	# We aren't searching for YOU or SAN
	planets.remove('YOU')
	planets.remove('SAN')

    # There should only be one planet each
	start = edges['YOU'][0]
	target = edges['SAN'][0]
	visited = set()
	node = start
	to_visit = deque()

	paths = {node: [node]}
	while node != target:
		visited.add(node)
		for n in edges[node]:
			if not n in visited:
				to_visit.append(n)
				paths[n] = paths[node] + [n]
		node = to_visit.popleft()

	return len(paths[target]) - 1

print(part1())
print(part2())


