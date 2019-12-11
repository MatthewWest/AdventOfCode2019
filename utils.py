def find_coordinate_bounds(list_of_tuples):
  max_x = float('-inf')
  min_x = float('inf')
  max_y = float('-inf')
  min_y = float('inf')
  for x, y in list_of_tuples:
    if x > max_x:
      max_x = x
    if x < min_x:
      min_x = x
    if y > max_y:
      max_y = y
    if y < min_y:
      min_y = y
  return min_x, max_x, min_y, max_y

def defaultdict_to_string(d, key):
  min_x, max_x, min_y, max_y = find_coordinate_bounds(d.keys())

  out = []
  for row in range(min_y, max_y+1):
    row_str = []
    for col in range(min_x, max_x+1):
      pos = (col, row)
      row_str.append(key[d[pos]])
    out.append(''.join(row_str))
  return '\n'.join(out)
