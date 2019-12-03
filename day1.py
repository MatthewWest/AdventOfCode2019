from math import floor

def fuel_required(mass):
	return floor(mass/3) - 2

def get_input_string():
	with open('day1input.txt') as f:
		return f.read()

def part1():
	input_list = [int(x) for x in get_input_string().splitlines()]
	total = 0
	for m in input_list:
		total += fuel_required(m)
	return total

def fuel_required_including_fuel(mass):
	total_fuel = 0
	fuel = fuel_required(mass)
	while fuel >= 0:
		total_fuel += fuel
		fuel = fuel_required(fuel)
	return total_fuel

def part2():
	input_list = [int(x) for x in get_input_string().splitlines()]
	total = 0
	for m in input_list:
		total += fuel_required_including_fuel(m)
	return total

print(part1())
print(part2())