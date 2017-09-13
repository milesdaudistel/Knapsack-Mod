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

  #all items are now sorted by value density, and all useless items have been removed
  items = [item for item in items if item[4]-item[3] > 0 and item[2] < P and item[3] < M]
  items = sorted(items, key=lambda x: (x[2]/(x[4]-x[3])) )

  if mode == "full_solve":
    adjacency_matrixer(P, M, N, C, items, constraints, file_num)
    heuristic_num_constraints(P, M, N, C, items, constraints, file_num)
    return heuristic_average_value_density(P, M, N, C, items, constraints, file_num)
  elif mode == "choose_classes":
    heuristic_num_constraints(P, M, N, C, items, constraints, file_num)
    return heuristic_average_value_density(P, M, N, C, items, constraints, file_num)
  else:
    '''
    matrix_file = "matrices/matrix" + file_num + ".p"
    adjacency_matrix = pickle.load( open( matrix_file, "rb" ) )

    classes = make_list_of_classes(items, file_num, adjacency_matrix)

    class_values_profit_density = class_heuristic_average_profit_density(classes)

    chosen_classes = choose_classes(adjacency_matrix, class_values_profit_density)

    return choose_items_greedily(P, M, N, C, items, chosen_classes, file_num)
    '''
    return heuristic_decider(P, M, N, C, items, file_num)

def heuristic_decider(P, M, N, C, items, file_num):
  matrix_file = "matrices/matrix" + file_num + ".p"
  adjacency_matrix = pickle.load( open( matrix_file, "rb" ) )

  classes = make_list_of_classes(items, file_num, adjacency_matrix)

  tot_prof_sort, avg_prof_sort, tot_prof_density_sort, avg_prof_density_sort = god_class_sorting_heuristic(classes)

  tot_prof_classes = choose_classes(adjacency_matrix, tot_prof_sort)
  avg_prof_classes = choose_classes(adjacency_matrix, avg_prof_sort)
  tot_prof_density_classes = choose_classes(adjacency_matrix, tot_prof_density_sort)
  avg_prof_density_classes = choose_classes(adjacency_matrix, avg_prof_density_sort)

  tot_prof_items, tot_prof_money = choose_items_greedily(P, M, N, C, items, tot_prof_classes, file_num)
  avg_prof_items, avg_prof_money = choose_items_greedily(P, M, N, C, items, avg_prof_classes, file_num)
  tot_prof_density_items, tot_prof_density_money = choose_items_greedily(P, M, N, C, items, tot_prof_density_classes, file_num)
  avg_prof_density_items, avg_prof_density_money = choose_items_greedily(P, M, N, C, items, avg_prof_density_classes, file_num)

  winner = max([tot_prof_money, avg_prof_money, tot_prof_density_money, avg_prof_density_money])
  if winner == tot_prof_money:
    print("Problem " + file_num + " best solved by total profit heuristic with a total of " + str(tot_prof_money))
    return tot_prof_items
  elif winner == avg_prof_money:
    print("Problem " + file_num + " best solved by average profit heuristic with a total of " + str(avg_prof_money))
    return avg_prof_items
  elif winner == tot_prof_density_money:
    print("Problem " + file_num + " best solved by total profit density heuristic with a total of " + str(tot_prof_density_money))
    return tot_prof_density_items
  #elif winner == avg_prof_density_money:
  else:
    print("Problem " + file_num + " best solved by average profit density heuristic with a total of " + str(avg_prof_density_money))
    return avg_prof_density_items

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


#problem 7 2075348129.0
#problem 10 869796.4500000004

def make_list_of_classes(items, file_num, adjacency_matrix):
  highest_num_class = 0
  for item in items:
    if item[1] > highest_num_class:
      highest_num_class = item[1]

  classes = [[] for _ in range(highest_num_class+1)]
  for item in items:
    classes[item[1]] += [item]

  #delete empty classes
  classes = [class_i for class_i in classes if class_i != []]
  return classes

#used to be (P, M, N, C, items, constraints, file_num, adjacency_matrix, classes_sorted_by_heuristic_value)
def choose_classes(adjacency_matrix, classes_sorted_by_heuristic_value):
  chosen_classes = []
  while len(classes_sorted_by_heuristic_value) > 0:
    chosen_class = classes_sorted_by_heuristic_value[0]
    chosen_classes += [chosen_class]
    constraint = adjacency_matrix[chosen_class]
    classes_sorted_by_heuristic_value = [class_i for class_i in classes_sorted_by_heuristic_value if class_i not in constraint]

  return chosen_classes

def god_class_sorting_heuristic(classes):
  class_values_total_profit = []
  class_values_average_profit = []
  class_values_total_profit_density = []
  class_values_average_profit_density = []
  for class_i in classes:
    class_i_total_profit = sum([(item[4]-item[3]) for item in class_i])
    class_i_average_profit = class_i_total_profit / len(class_i)

    class_i_total_profit_density = sum([(item[4]-item[3])/(item[2] + 0.001) for item in class_i])
    class_i_average_profit_density = class_i_total_profit_density / len(class_i)



    #class_i contains all items of class i, so in order to get the name of class i, have to do class_i[0][1]
    class_name = class_i[0][1]
    class_values_total_profit += [(class_name, class_i_total_profit)]
    class_values_average_profit += [(class_name, class_i_average_profit)]
    class_values_total_profit_density += [(class_name, class_i_total_profit_density)]
    class_values_average_profit_density += [(class_name, class_i_average_profit_density)]

  class_values_total_profit = sorted(class_values_total_profit, key=lambda x: 1 / x[1] )
  class_values_average_profit = sorted(class_values_average_profit, key=lambda x: 1 / x[1] )
  class_values_total_profit_density = sorted(class_values_total_profit_density, key=lambda x: 1 / x[1] )
  class_values_average_profit_density = sorted(class_values_average_profit_density, key=lambda x: 1 / x[1] )

  class_values_total_profit = [class_value[0] for class_value in class_values_total_profit]
  class_values_average_profit = [class_value[0] for class_value in class_values_average_profit]
  class_values_total_profit_density = [class_value[0] for class_value in class_values_total_profit_density]
  class_values_average_profit_density = [class_value[0] for class_value in class_values_average_profit_density]
  return class_values_total_profit, class_values_average_profit, class_values_total_profit_density, class_values_average_profit_density

def choose_items_greedily(P, M, N, C, items, classes_to_choose_from, file_num):
  items_to_choose_from = [item for item in items if item[1] in classes_to_choose_from]
  items_chosen = []
  total_profit = 0
  for item in items_to_choose_from:
    p = item[2]
    m = item[3]
    if P >= p and M >= m:
      #only need the names of the items
      items_chosen += [item[0]]
      total_profit += item[4] - item[3]
      P -= p
      M -= m

  #print("Problem " + file_num + " total money: " + str(M + total_profit))
  #print("Problem " + file_num + " leftover weight: " + str(P))

  return (items_chosen, M + total_profit)


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
  for item_index in range(len(items_to_choose_from_sorted)):
    possible_item = items_to_choose_from_sorted[item_index]
    p = possible_item[2]
    m = possible_item[3]
    if P >= p and M >= m:
      #only need the names of the items
      items_chosen += [possible_item[0]]
      total_resale += possible_item[4]
      P -= p
      M -= m

  picked_classes_file = "picked_classes/picked_classes" + file_num + ".p"

  total_profit_file = "output/total_profit" + file_num + ".p"
  pickle.dump( total_profit, open( total_profit_file, "wb" ) )

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