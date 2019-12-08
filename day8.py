width = 25
height = 6
filename = 'day8input.txt'

def get_layers(input, xsize, ysize):
  layers = []
  size=xsize*ysize
  for i in range(0, len(input), size):
    layers.append([int(c) for c in input[i:i+size]])
  return layers


def part1():
  layers = get_layers(open(filename).read().rstrip(), width, height)

  all_counts = []
  for layer in layers:
    digit_counts = {}
    for i in range(10):
      digit_counts[i] = 0
    for x in layer:
      digit_counts[x] = digit_counts[x] + 1
    all_counts.append(digit_counts)

  least = None
  least_zeros = float("inf")
  for i, counts in enumerate(all_counts):
    if counts[0] < least_zeros:
      least_zeros = counts[0]
      least = i

  return all_counts[least][1] * all_counts[least][2]



def initialize_output(xsize, ysize):
  output = []
  for y in range(ysize):
    row = []
    for x in range(xsize):
      row.append(None)
    output.append(row)  
  return output


def make_image(input, xsize, ysize):
  layers = get_layers(input, xsize, ysize)
  output = initialize_output(xsize, ysize)

  for layer in layers:
    for y in range(ysize):
      for x in range(xsize):
        if output[y][x] is None:
          val = layer[y*xsize + x]
          if val != 2:
            output[y][x] = val
  return output

def format_output(output):
  lines = []
  for row in output:
    rep = []
    for val in row:
      if val == 0:
        rep.append(' ')
      else:
        rep.append('*')
    lines.append(''.join(rep))
  return '\n'.join(lines)


def part2():
  output = make_image(open(filename).read().rstrip(), width, height)
  return format_output(output)


print(part1())
print(part2())
