
def get_input():
	with open('day4input.txt') as f:
		r = f.read().split('-')
	return int(r[0]), int(r[1])


def part1_condition(n):
	s = str(n)
	prev = 0
	repeated = False
	nRepeats = 1
	for c in s:
		digit = int(c)
		if digit < prev:
			return False

		if digit == prev:
			nRepeats += 1
		else:
			if nRepeats >= 2:
				repeated = True
			nRepeats = 1

		prev = digit
	if nRepeats >= 2:
		repeated = True
	return repeated


def part1():
	low, high = get_input()
	count = 0
	for i in range(low, high + 1):
		if part1_condition(i):
			count += 1
	return count


def part2_condition(n):
	s = str(n)
	prev = 0
	repeated = False
	repeatedOutsideString = False
	nRepeats = 1
	for c in s:
		digit = int(c)
		if digit < prev:
			return False

		if digit == prev:
			nRepeats += 1
		else:
			if nRepeats == 2:
				repeatedOutsideString = True
			nRepeats = 1

		prev = digit
	if nRepeats == 2:
		repeatedOutsideString = True
	return repeatedOutsideString


def part2():
	low, high = get_input()	
	count = 0
	for i in range(low, high + 1):
		if part2_condition(i):
			count += 1
	return count


print(part1())
print(part2())