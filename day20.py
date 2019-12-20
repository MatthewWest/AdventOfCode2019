from collections import defaultdict, deque
from utils import defaultdict_repr, find_coordinate_bounds

def parse_input(s):
	m = defaultdict(lambda: '#')
	for y, line in enumerate(s.splitlines()):
		ymax = y
		for x, c in enumerate(line):
			m[(x, y)] = c
			xmax = x
	portal_endpoints = defaultdict(lambda: [])
	for y in range(ymax):
		for x in range(xmax):
			if m[(x, y)].isalpha():
				c = m[(x, y)]
				left = (x-1, y)
				right = (x+1, y)
				up = (x, y-1)
				down = (x, y+1)
				token = None
				# Only add tokens from the letter next to the maze
				if m[left] == '.':
					square = left
					token = c + m[right]
				elif m[right] == '.':
					square = right
					token = m[left] + c
				elif m[up] == '.':
					square = up
					token = c + m[down]
				elif m[down] == '.':
					square = down
					token = m[up] + c
				if token:
					portal_endpoints[token].append(square)
	return m, portal_endpoints


s1 = '''         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       '''


def get_portals(endpoints):
	portals = {}
	for name in endpoints:
		connected = endpoints[name]
		if len(connected) > 1:
			portals[connected[0]] = connected[1]
			portals[connected[1]] = connected[0]
	return portals


def get_neighbors(m, pos, portals):
	x, y = pos
	dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
	neighbors = []
	for dx, dy in dirs:
		if m[(x+dx, y+dy)] == '.':
			neighbors.append((x+dx, y+dy))
	if pos in portals:
		neighbors.append(portals[pos])
	return neighbors


def bfs(m, start, end, portals):
	q = deque()
	visited = set()
	q.append((start, 0))
	while q:
		p, dist = q.popleft()
		if p == end:
			return dist
		visited.add(p)
		for n in get_neighbors(m, p, portals):
			if n in visited:
				continue
			q.append((n, dist+1))
	return None


def part1():
	s = open('day20input.txt').read()
	m, endpoints = parse_input(s)
	portals = get_portals(endpoints)
	return bfs(m, endpoints['AA'][0], endpoints['ZZ'][0], portals)


def get_recursive_portals(endpoints, xmax, ymax):
	in_portals = {}
	out_portals = {}
	for name in endpoints:
		connected = endpoints[name]
		if len(connected) == 2:
			x1, y1 = connected[0]
			x2, y2 = connected[1]
			if x1 <= 2 or x1 >= xmax - 3 or y1 <= 2 or y1 >= ymax - 3:
				outer = x1, y1
				inner = x2, y2
			else:
				outer = x2, y2
				inner = x1, y1
			in_portals[inner] = outer
			out_portals[outer] = inner
	return in_portals, out_portals


def get_recursive_neighbors(m, pos, in_portals, out_portals):
	x, y, level = pos
	dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
	neighbors = []
	for dx, dy in dirs:
		if m[(x+dx, y+dy)] == '.':
			neighbors.append((x+dx, y+dy, level))

	if (x, y) in in_portals:
		xnew, ynew = in_portals[(x, y)]
		neighbors.append((xnew, ynew, level+1))
	elif (x, y) in out_portals and level > 0:
		xnew, ynew = out_portals[(x, y)]
		neighbors.append((xnew, ynew, level-1))
	return neighbors


def bfs_recursive_maze_path(m, start, end, in_portals, out_portals):
	q = deque()
	visited = set()
	q.append((start, []))
	while q:
		p, path = q.popleft()
		if p == end:
			return path
		visited.add(p)
		for n in get_recursive_neighbors(m, p, in_portals, out_portals):
			if n in visited:
				continue
			q.append((n, path + [n]))
	return None


def bfs_recursive_maze(m, start, end, in_portals, out_portals):
	q = deque()
	visited = set()
	q.append((start, 0))
	while q:
		p, dist = q.popleft()
		if p == end:
			return dist
		visited.add(p)
		for n in get_recursive_neighbors(m, p, in_portals, out_portals):
			if n in visited:
				continue
			q.append((n, dist + 1))
	return None


s3 = '''             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     '''


def map_square_to_endpoint(endpoints):
	names = {}
	for tok in endpoints:
		squares = endpoints[tok]
		for s in squares:
			names[s] = tok
	return names


def print_path(path, endpoints):
	square_names = map_square_to_endpoint(endpoints)
	x, y, l = path[0]
	start = 'AA'
	n = 0
	for step in path:
		x1, y1, l1 = step
		n += 1
		if (x1, y1) in square_names and l1 == l:
			end = square_names[(x1, y1)]
			print("Walk from {:} to {:} ({:} steps)".format(start, end, n))
			start = end
			n = 0

		if l1 > l:
			print("Recurse into level {:} through {:} (1 step)".format(l1, square_names[(x1, y1)]))
			n = 0
		elif l1 < l:
			print("Return to level {:} through {:} (1 step)".format(l1, square_names[(x1, y1)]))
			n = 0
		x, y, l = x1, y1, l1



def part2():
	s = open('day20input.txt').read()
	m, endpoints = parse_input(s)
	_, xmax, _, ymax = find_coordinate_bounds(m.keys())
	in_portals, out_portals = get_recursive_portals(endpoints, xmax, ymax)
	x, y = endpoints['AA'][0]
	start = (x, y, 0)
	x, y = endpoints['ZZ'][0]
	end = (x, y, 0)
	dist = bfs_recursive_maze(m, start, end, in_portals, out_portals)
	return dist

print(part1())
print(part2())