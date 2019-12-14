from math import ceil

class Ingredient():
  def __init__(self, tag, quantity):
    self._tag = tag
    self._quantity = quantity

  @property
  def tag(self):
    return self._tag

  @property
  def quantity(self):
    return self._quantity

  def __repr__(self):
    return '{:} {:}'.format(self._quantity, self._tag)

  def __eq__(self, other):
    return self.tag == other.tag and self.quantity == other.quantity

  def __hash__(self):
    return hash((self.tag, self.quantity))
  

class Recipe():
  def __init__(self, output, ingredients):
    self._output = output
    self._ingredients = ingredients

  @property
  def output(self):
    return self._output

  @property
  def ingredients(self):
    return self._ingredients

  def __repr__(self):
    return '\n' + ', '.join([str(i) for i in self._ingredients]) + ' => ' + str(self._output)
  


def parse_ingredient(s):
  parts = s.split(' ')
  return Ingredient(parts[1], int(parts[0]))


def parse_input(s):
  lines = s.splitlines()
  recipes = []
  for line in lines:
    parts = line.split('=>')
    inputs = [parse_ingredient(i.strip()) for i in parts[0].split(',')]
    output = parse_ingredient(parts[1].strip())
    recipes.append(Recipe(output, inputs))
  return recipes

def get_input():
  with open('day14input.txt') as f:
    return f.read()


def build_dag(recipes):
  components = {}
  for recipe in recipes:
    if recipe._output.tag in components:
      raise Exception
    components[recipe._output.tag] = recipe
  return components


def ore_needed(components, free, tag, quantity):
  # Reuse existing materials
  if tag in free:
    if free[tag] >= quantity:
      # surplus already, return 0 and remove from available
      free[tag] -= quantity
      return 0
    else:
      quantity -= free[tag]
      free[tag] = 0

  recipe = components[tag]
  recipe_multiplier = ceil(quantity / recipe.output.quantity)
  recipe_leftover = recipe_multiplier * recipe.output.quantity - quantity
  if tag in free:
    free[tag] += recipe_leftover
  else:
    free[tag] = recipe_leftover

  # Base case
  if len(recipe.ingredients) == 1 and recipe.ingredients[0].tag == 'ORE':
    return recipe.ingredients[0].quantity * recipe_multiplier  
  # Recursive case
  ore = 0
  for ingredient in recipe.ingredients:
    ore += ore_needed(components, free, ingredient.tag, ingredient.quantity * recipe_multiplier)
  return ore


s1 = '''9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL'''

s2 = '''157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT'''

s3 = '''171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX'''

def part1():
  recipes = parse_input(get_input())
  components = build_dag(recipes)
  return ore_needed(components, {}, 'FUEL', 1)


def can_produce(components, free, tag, quantity):
  # Reuse existing materials
  if tag in free:
    if free[tag] >= quantity: # surplus, return True and remove from available
      free[tag] -= quantity
      return True
    else:
      quantity -= free[tag]
      free[tag] = 0
      if tag == 'ORE':  # If we get here we didn't have any ORE left
        return False

  recipe = components[tag]
  recipe_multiplier = ceil(quantity / recipe.output.quantity)
  recipe_leftover = recipe_multiplier * recipe.output.quantity - quantity
  if tag in free:
    free[tag] += recipe_leftover
  else:
    free[tag] = recipe_leftover

  # Recursive case
  for ingredient in recipe.ingredients:
    if not can_produce(components, free, ingredient.tag, ingredient.quantity * recipe_multiplier):
      return False
  return True


def part2():
  recipes = parse_input(get_input())
  components = build_dag(recipes)

  a = 1
  b = 1
  while can_produce(components, {'ORE': 1000000000000}, 'FUEL', b):
    a = b
    b = a*2

  while b > a + 1:
    mid = a + (b-a)//2
    if can_produce(components, {'ORE': 1000000000000}, 'FUEL', mid):
      a = mid
    else:
      b = mid
  return a


print(part1())
print(part2())
