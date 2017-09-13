#!/usr/bin/env python

from __future__ import division
import argparse
import pickle


"""
===============================================================================
  Please complete the following function.
===============================================================================
"""

def solve(P, M, N, C, items, constraints, mode, input_file):
  """
  Write your amazing algorithm here.

  Return: a list of strings, corresponding to item names.
  """
  #P = pounds
  #M = money
  #N = num items
  #C = num constraints
  input_file_digits = [s for s in list(input_file) if s.isdigit()]
  file_num = "".join(input_file_digits)

  if mode == "full_solve":
    adjacency_matrixer(P, M, N, C, items, constraints, file_num)
    heuristic_num_constraints(P, M, N, C, items, constraints, file_num)
    return heuristic_average_value_density(P, M, N, C, items, constraints, file_num)
  elif mode == "choose_classes":
    heuristic_num_constraints(P, M, N, C, items, constraints, file_num)
    return heuristic_average_value_density(P, M, N, C, items, constraints, file_num)
  else:
    return heuristic_average_value_density(P, M, N, C, items, constraints, file_num)

def adjacency_matrixer(P, M, N, C, items, constraints, file_num):
  print("hang0")
  list_of_all_classes = []
  for i in items:
    #[item_name]; [class]; [weight]; [cost]; [resale value]
    if i[1] not in list_of_all_classes:
      list_of_all_classes += [i[1]]
  #list_of_all_classes = list(filter(None, list_of_all_classes))
  #list_of_all_classes.sort()
  num_classes = max(list_of_all_classes)

  print("hang1")

  adjacency_matrix = [[] for _ in range(num_classes+1)]
  for current_class in list_of_all_classes:
    for constraint in constraints:
      if current_class in constraint:
        adjacency_matrix[current_class] += constraint

  print("hang2")

  #gets rid of all instances of class_i in the adjacency list of node i
  #also sorts in ascending order, and removes duplicates
  for class_index in range(num_classes+1):
    constraint_i = adjacency_matrix[class_index]
    constraint_i = [class_i for class_i in constraint_i if class_i != class_index]
    constraint_i = list(set(constraint_i))
    constraint_i.sort()
    #put the class as the first thing in its own adjacency list so the file is easier to read
    constraint_i = [class_index] + constraint_i
    adjacency_matrix[class_index] = constraint_i

  matrix_file = "matrices/matrix" + file_num + ".p"
  pickle.dump( adjacency_matrix, open( matrix_file, "wb" ) )
  return adjacency_matrix

def heuristic_num_constraints(P, M, N, C, items, constraints, file_num):
  #choose class with the least # of constraints until you can no longer choose classes
  #TRY MOST NUMBER OF CONSTRAINTS NEXT??
  #adjacency_matrix, num_classes = get_adjacency_matrix(P, M, N, C, items, constraints)
  matrix_file = "matrices/matrix" + file_num + ".p"
  adjacency_matrix = pickle.load( open( matrix_file, "rb" ) )
  #find the list in the adjacency matrix with the smallest length (the least number of constraints)
  #remove all classes that it conflicts with from the total classes list, put the class index into list of used classes
  classes_picked = []
  while len(adjacency_matrix) > 0:
    #go through adjacency matrix, looking for the list with smallest length that isn't 0
    smallest_len = 100000000000
    smallest_index = 0
    for class_index in range(len(adjacency_matrix)):
      current_list = adjacency_matrix[class_index]
      if len(current_list) < smallest_len and len(current_list) > 0:
        smallest_len = len(current_list)
        smallest_index = class_index

    #pick that list
    picked_list = adjacency_matrix[smallest_index]

    
    #put first item into classes_picked
    classes_picked += [adjacency_matrix[smallest_index][0]]

    #the rest cannot be used
    #delete each list in adjacency_matrix that starts with one of the numbers in the adjacency list that you picked
    #do this by first turning it into a blank list, since deleting it outright will mess up the iterating of the for loop
    for class_index in range(len(adjacency_matrix)):
      if adjacency_matrix[class_index][0] in picked_list:
        adjacency_matrix[class_index] = []

    #get rid of the empty lists you made
    adjacency_matrix = [adj_list for adj_list in adjacency_matrix if adj_list != []]

  picked_classes_file = "picked_classes/picked_classes" + file_num + ".p"
  pickle.dump( classes_picked, open( picked_classes_file, "wb" ) )

def heuristic_treat_class_as_single_item(P, M, N, C, items, constraints, file_num):
	#heuristic num constraints takes care of imcompatible classes for you
	#sort items by class, calculate mean value density for that
	#remember to remove all items with negative value
  classes = [[] for _ in range(len(items))]
  for i in items:
    classes[i[1]] += [i]

  #delete empty classes
  classes = [class_i for class_i in classes if class_i != []]

  #for each class in classes, average the value density, discarding all useless items
  classes_as_items = []
  for class_i in classes:
    class_name = class_i[0][1]
    total_resale = 0
    total_cost = 0
    total_weight = 0
    for item in class_i:
      if item[4] - item[3] > 0:
        total_resale += item[4]
        total_cost += item[3]
        total_weight += item[2]
    class_i_as_item = [class_name, class_name, total_weight/len(class_i), total_cost/len(class_i), total_resale/len(class_i)]
    classes_as_items += [class_i_as_item]

  classes_as_items = sorted(classes_as_items, key=lambda x: (x[2]/(x[4]-x[3])))

  #come back to this later, its probably more worth your time to do the genetic algorithm
  return classes_as_items


def heuristic_average_value_density(P, M, N, C, items, constraints, file_num):
  picked_classes_file = "picked_classes/picked_classes" + file_num + ".p"
  classes_picked = pickle.load( open( picked_classes_file, "rb" ) )

  #dont think you need sorted items just yet
  #first just choose valid items from the regular list (items), only including them if their class is in classes_picked
  #if statement is to get rid of items that would cause division by 0 error.  Doesn't matter since they cost more than they're worth
  items_to_choose_from = [item for item in items if item[1] in classes_picked if item[4]-item[3] > 0]

  items_to_choose_from_sorted = sorted(items_to_choose_from, key=lambda x: (x[2]/(x[4]-x[3])) )

  items_chosen = []
  total_resale = 0
  #total_profit = 0
  for item_index in range(len(items_to_choose_from_sorted)):
    possible_item = items_to_choose_from_sorted[item_index]
    p = possible_item[2]
    m = possible_item[3]
    if P >= p and M >= m:
      #only need the names of the items
      items_chosen += [possible_item[0]]
      total_resale += possible_item[4]
      #total_profit += (possible_item[4]-possible_item[3])
      P -= p
      M -= m

  print("total money: " + str(M+total_resale))

  picked_classes_file = "picked_classes/picked_classes" + file_num + ".p"

  #total_profit_file = "output/total_profit" + file_num + ".p"
  #pickle.dump( total_profit, open( total_profit_file, "wb" ) )

  return items_chosen

"""
===============================================================================
  No need to change any code below this line.
===============================================================================
"""

def read_input(filename):
  """
  P: float pounds
  M: float money
  N: integer num items
  C: integer num constraints
  items: list of tuples
  constraints: list of sets
  """
  with open(filename) as f:
    P = float(f.readline())
    M = float(f.readline())
    N = int(f.readline())
    C = int(f.readline())
    items = []
    constraints = []
    for i in range(N):
      name, cls, weight, cost, val = f.readline().split(";")
      items.append((name, int(cls), float(weight), float(cost), float(val)))
    for i in range(C):
      constraint = set(eval(f.readline()))
      constraints.append(constraint)
  return P, M, N, C, items, constraints

def write_output(filename, items_chosen):
  with open(filename, "w") as f:
    for i in items_chosen:
      f.write("{0}\n".format(i))

if __name__ == "__main__":

  parser = argparse.ArgumentParser(description="PickItems solver.")
  parser.add_argument("input_file", type=str, help="____.in")
  parser.add_argument("output_file", type=str, help="____.out")
  parser.add_argument("mode", type=str, help="____.dongus")
  args = parser.parse_args()

  P, M, N, C, items, constraints = read_input(args.input_file)
  mode = args.mode
  items_chosen = solve(P, M, N, C, items, constraints, mode, args.input_file)
  write_output(args.output_file, items_chosen)