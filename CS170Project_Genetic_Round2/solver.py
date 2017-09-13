#!/usr/bin/env python

from __future__ import division
import argparse
import pickle
import random


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
  #[item_name]; [class]; [weight]; [cost]; [resale value]
  input_file_digits = [s for s in list(input_file) if s.isdigit()]
  file_num = "".join(input_file_digits)

  if mode == -1:
    adjacency_matrixer(P, M, N, C, items, constraints, file_num)
    return heuristic_pick_random(P, M, N, C, items, constraints, file_num)
  elif mode == -2:
  	return check_random_solution(P, M, N, C, items, constraints, file_num)
  elif mode == -3:
  	return init_gen(P, M, N, C, items, constraints, file_num)
  elif mode == -4:
  	return class_matrixer(P, M, N, C, items, constraints, file_num)
  elif mode == -5:
  	return genetic_alg(P, M, N, C, items, constraints, file_num)
  else:
    population_size = 25
    for i in range(population_size):
      chromosome = heuristic_pick_random(P, M, N, C, items, constraints, file_num)
      chromosome_file_name = "population/problem" + file_num + "chromosome" + str(i + mode) + ".p"
      pickle.dump( chromosome, open( chromosome_file_name, "wb" ) )

    return heuristic_pick_random(P, M, N, C, items, constraints, file_num)


'''
CHANGE ADJACENCY MATRIX TO ACTUALLY BE MATRIX???
maybe you just need to alter the list of adjacency lists you already have

mutation rate = 0.001????
100-200 population size?
'at least 30' according to some random article from 1993
tournament size is 5.... lets change it to 10
want more pressure to select stronger chromosomes, since we'll have to randomly combine them later
just do the tournament until you have 96 children
keep the best 4 original

initialize array containing all 100 chromosomes
assign fitness value to all chromosomes
do tournament selection
breed chromosomes

tournament selection:
	choose 10 chromosomes randomly
	choose the fittest from these 10, add it to the breeding tank

	how to assign fitness:
		sum the resale - cost for each item

	how to breed chromosomes:
		lets use 4 parents just for fun
		randomly select a class from these 4 parents
		this is the seed class
		eliminate all conflicting classes from total class pool
		randomly select another class, eliminate all conflicting classes
		do this until there are no more classes to choose from
		check that solution is still feasible.  if not, remove items randomly until it is
		after all this is done, (and assuming the solution was originally feasible) see if there are any extra classes you could add
			if you can add more classes, do so, and see how many items from this class you can add
			set all incompatible class items to be 0
			this isn't exactly mutation since it would always make the chromosome more fit no matter what
			you can check if there are any extra classes you could add by taking inner product of the adjacency rows of
			all the included classes so far.  then check this new vector, and if there is a 1 at the index of any class
			that is not currently in the selection, that means you can add that class and it hasn't been added yet

			try this with the list of adjacency lists
			have a list containing all possible classes
			during breeding, choose a class, then take it and all incompatible classes out out a copy of the list of all classes

		keep 4 best chromosomes from last generation
'''

'''
#in the event that you reach genetic homogeny too soon, make tournament sizes smaller, or try making more parents
def genetic_alg(P, M, N, C, items, constraints, file_num):
	chromosomes, all_classes = init_gen
	items = items sorted by profit/weight
	for _ in range(number of generations to breed):
		breeding chromosomes = tournament(chromosomes)
		#the next gen
		chromosomes = breeding_algorithm(breeding chromosomes, all_classes)
		#chromosomes has 96 children, add best 4 from last gen
		chromosomes += [most fit 4 from last gen]

'''
def genetic_alg(P, M, N, C, items, constraints, file_num):
	#sorts items by value density worst to best
	#for item in items:
	#	print(item[1])
	#	print((item[4]-item[3])/item[2])
	list_of_all_classes = []
	for i in items:
	#[item_name]; [class]; [weight]; [cost]; [resale value]
		if i[1] not in list_of_all_classes:
			list_of_all_classes += [i[1]]

	items = [item for item in items if item[4] - item[3] < 0]
	#items = [item for item in items if item[4] - item[3] != 0]
	sorted_items = sorted(items, key=lambda x: (x[2] /(x[4]-x[3]) ))
	#reverses list order
	#sorted_items.reverse()

	class_matrix_file = "real_matrices/matrix" + file_num + ".p"
	class_matrix = pickle.load( open( class_matrix_file, "rb" ) )

	print("finished loading matrix")

	chromosomes = init_gen(P, M, N, C, items, constraints, file_num)
	#first solution, first item, name of first item
	#prints 'revolutionary lots'
	#print(str(chromosomes[0][0][0]))
	
	number_of_generations = 200
	tournament_size = 1
	parents_per_child = 4
	amount_elitism = 1
	num_tournaments = (parents_per_child * (100 - amount_elitism))

	for gen in range(number_of_generations):
		breeding_pool = []
		for _ in range(num_tournaments):
			breeding_pool += [tournament(P, M, chromosomes, tournament_size)]
		next_gen = breeding_algorithm(P, M, breeding_pool, parents_per_child, class_matrix, sorted_items, list_of_all_classes) 
		
		old_best_chromosome = elitism(P, M, chromosomes, 1)[0]

		chromosomes = next_gen + elitism(P, M, chromosomes, amount_elitism)
		if len(chromosomes) != 100:
			print("population grew to be " + str(len(chromosomes)))
			x = 1 / 0
		print("gen: " + str(gen) + " completed")

		new_best_chromosome = elitism(P, M, chromosomes, 1)[0]
		old_best_fitness = assess_fitness(P, M, old_best_chromosome)
		new_best_fitness = assess_fitness(P, M, new_best_chromosome)
		if new_best_fitness > old_best_fitness:
			print("most fit chromosome has been replaced, " + str(new_best_fitness) + " vs " + str(old_best_fitness))


	#done breeding, output best result
	fittest = []
	best_score = 0
	for chromosome in chromosomes:
		fittness = assess_fitness(P, M, chromosome)
		if fittness > best_score:
			best_score = fittness
			fittest = chromosome

	print("problem " + file_num + " total money: " + str(M + best_score))
	return fittest










'''
def init_gen(P, M, N, C, items, constraints, file_num):
	get all chromosome files, convert them to 10100101010101 arrays
	put all chromosomes into chromosome array
	try pickling this array of all chromosomes
	create list of all possible classes to be passed to later functions
	return both
'''
def init_gen(P, M, N, C, items, constraints, file_num):
	chromosomes = []
	for i in range(100):
		chromosome_file = "population/problem" + file_num + "chromosome" + str(i) + ".p"
		chromosome = pickle.load( open( chromosome_file, "rb" ) )
		chromosomes += [chromosome]

	#no need to pickle, takes a second
	return chromosomes

def elitism(P, M, chromosomes, amount_saved):
	#contains tuples of (chromosome, fitness)
	if amount_saved == 0:
		return []
	veterans = [([], -1) for _ in range(amount_saved)]
	#have to sort the whole list anyway
	#consider if you sort everything but the last 1, what if that last 1 was the the most fit out of all of them?
	#sort them from most to least fit
	chromosomes_ranked = sorted(chromosomes, key=lambda x: assess_fitness(P, M, x))

	#return last x elements of array
	return chromosomes_ranked[-1 * amount_saved:]


'''
def tournament(chromosomes, tournament_size):
	choose 10 random chromosomes
	assign fitness values to each using fitness function
	pick the most fit chromosome, add it to array of breeding chromosomes
	do this until you have 96*4=384 chromosomes
	return the array of chromosomes
'''
def tournament(P, M, chromosomes, tournament_size):
	top_chromosome = []
	top_fitness = 0
	for _ in range(tournament_size):
		contender = chromosomes[random.randint(0, len(chromosomes)-1)]
		contender_fitness = assess_fitness(P, M, contender)
		if contender_fitness > top_fitness:
			top_chromosome = contender
			top_fitness = contender_fitness
	return top_chromosome

def assess_fitness(P, M, chromosome):
	resale = sum([x[4] for x in chromosome])
	cost = sum([x[3] for x in chromosome])
	weight = sum([x[2] for x in chromosome])
	#chromosome is not a feasible solution
	if weight > P or cost > M:
		return -1
	else:
		return resale - cost

'''
#do it randomly
#afterwords we can try a faster solution where chromosomes consist of random classes,
#but after class selection, we choose individual items greedily
def breeding_algorithm(breeding chromosomes, parents per child, all_classes):
	#parents per child default is 4
	next_gen = []
	for i in range(0, len(breeding chromosomes), parents per child):
		breed chromosomes[i] + chromosomes[i+1] + chromosomes[i+2] + chromosomes[i+3]
			gene pool = classes from all 4 parents 
			randomly choose a class as seed gene (make sure to include which parent it's from)
			remove all conflicting genes from gene pool
			remove seed gene and all conflicting genes from all_classes
			repeat until gene pool is empty
			#check if all_classes is empty
			#don't add any classes, this is just a greedy heuristic will be computationally hard
			#and won't give much additional benefit
	return next_gen
'''

def breeding_algorithm(P, M, breeding_pool, parents_per_child, class_matrix, items, all_classes):
	next_gen = []
	for i in range(0, len(breeding_pool), parents_per_child):
		class_pool = []
		
		#if you find that breeding is too biased towards the first class you pick, try tournament breeding
		#split class pool into 2 and 2 parents.  Pick from 1 class pool, then pick from the other
		#Or pick from parent 1, then from parent 2, then from parent 3, then from parent 4, then parent 1, until all classes are exhausted
		#parents = []
		#for j in range(i, i+parents_per_child):
		#	parents += [breeding_pool[j]]

		#class_pool = mating_algorithm(parents)

		parent1 = breeding_pool[i]
		parent2 = breeding_pool[i+1]
		parent3 = breeding_pool[i+2]
		parent4 = breeding_pool[i+3]
		#class_pool = [item[1] for item in parent1] + [item[1] for item in parent2] + [item[1] for item in parent3] + [item[1] for item in parent4]
		#class_pool = list(set(class_pool))
		'''
		kids_classes = []
		while len(class_pool) > 0:
			chosen_class = class_pool[random.randint(0, len(class_pool)-1)]
			kids_classes += [chosen_class]
			constraint = class_matrix[chosen_class]
			#delete all conflicting classes so it can't be chosen again
			#class_matrix[chosen_class][chosen_class] = 0
			class_pool = [class_i for class_i in class_pool if class_matrix[chosen_class][class_i] == 1]
			#all_classes = [class_i for class_i in all_classes if class_matrix[chosen_class][class_i] == 1]
		'''
		#right now this is nearly useless because you're pretty much guarenteed to get all the classes you need since selecting
		#the first class pretty much deletes everything
		#if len(all_classes) > 0:
			#print("there are unused classes")
			#kids_classes += all_classes
		parents = [parent1, parent2, parent3, parent4]
		kids_classes = kid_algorithm(parents, class_matrix)



		#now have all the kids classes, we need to choose the actual items of the kid
		#just do it greedily for now, can come back to this later
		#items are already sorted by profit/weight
		kid = []

		for item in items:
			if item[1] in kids_classes:
				kid += [item]
				P -= item[2]
				M -= item[3]
			if P < 0 or M < 0:
				#delete last item from kid, since this was the item that tipped it over into being an infeasible solution
				kid = kid[:-1]
				break

		next_gen += [kid]


	return next_gen

def kid_algorithm(parents, class_matrix):
	#takes in list of parents, returns kids classes
	parents_classes = [[item[1] for item in parent] for parent in parents]
	kids_classes = []

	#select parent randomly, select a class from that parent
	#temporarily remove that parent from rotation, and select another parent
	#remove parent by creating a copy of parents_classes without the parent you originally selected from
	#choose parents from the copy until there are no parents left

	#generate random list of indices, choose classes from parents in this order
	#repeat until parents_classes are empty, no need to create copy
	#this way has less bias than picking from a big list of all the classes, since the first class you
	#pick will heavily bias the child towards whichever parent or parents have that class



	while len(parents_classes) > 0:
		class_picking_order = [i for i in range(len(parents_classes))]
		random.shuffle(class_picking_order)
		for pick_ticket in class_picking_order:
			current_parent = parents_classes[pick_ticket]
			#print("len of current parent: " + str(len(current_parent)))
			#print("pickticket value: " + str(pick_ticket))
			chosen_class = []
			if len(current_parent) == 0:
				break
			elif len(current_parent) == 1:
				chosen_class = current_parent[0]
			else:
				chosen_class = current_parent[random.randint(0, len(current_parent)-1)]
			#delete all conflicting classes
			for parent_index in range(len(parents_classes)):
				parent_classes = parents_classes[parent_index]
				class_row = class_matrix[chosen_class]
				parents_classes[parent_index] = parenting_without_conflict(parent_classes, class_row)

			kids_classes += [chosen_class]
		parents_classes = [parent_classes for parent_classes in parents_classes if len(parent_classes) > 0]
	return kids_classes


def parenting_without_conflict(parent_classes, chosen_class_row):
	return [class_i for class_i in parent_classes if chosen_class_row[class_i]]



#the other adjacency_matrixer was actually a list of adjacency lists.....
def class_matrixer(P, M, N, C, items, constraints, file_num):
	max_class = 0
	for item in items:
		if item[1] > max_class:
			max_class = item[1]

	#for problem 1, max_class is 2999, and since its 0-2999, we need a matrix with 3000 entries
	class_matrix = [[1 for _ in range(max_class+1)] for _ in range(max_class+1)]
	#print("made empty matrix, max class is: " + str(max_class))
	#if a class doesn't exist, just leave it as 1
	#if its an empty class, it doesn't matter whether we include it or not
  #classes_with_at_least_one_item = []
  #for i in items:
    #[item_name]; [class]; [weight]; [cost]; [resale value]
    #if i[1] not in classes_with_at_least_one_item:
     # classes_with_at_least_one_item += [i[1]]
  #classes_with_no_items = [class_i for class_i in range(N) if class_i not in classes_with_at_least_one_item]




	for constraint in constraints:
		for item_class1 in constraint:
			for item_class2 in constraint:
				class_matrix[item_class1][item_class2] = 0
	matrix_file = "real_matrices/matrix" + file_num + ".p"
	pickle.dump( class_matrix, open( matrix_file, "wb" ) )
	return []



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
  #UNFINISHED
  #come back to this later, its probably more worth your time to do the genetic algorithm
  return classes_as_items

def heuristic_pick_random(P, M, N, C, items, constraints, file_num):
  matrix_file = "matrices/matrix" + file_num + ".p"
  adjacency_matrix = pickle.load( open( matrix_file, "rb" ) )

  """
  P: float pounds
  M: float money
  N: integer num items
  C: integer num constraints
  items: list of tuples
  constraints: list of sets
  """
  classes_picked = []
  while len(adjacency_matrix) > 0:
    random_class_index = random.randint(0, len(adjacency_matrix)-1)
    picked_class_row = adjacency_matrix[random_class_index]
    classes_picked += [picked_class_row[0]]

    #delete all rows corresponding to classes that are incompatible with the class that we have picked
    adjacency_matrix = [adj_row for adj_row in adjacency_matrix if adj_row[0] not in picked_class_row]


  #make sure item isn't one of the constrained items and it has positive resale value
  items_to_choose_from = [item for item in items if item[1] in classes_picked and item[4] > item[3]]
  #randomly shuffle the list so we can pick items sequentially
  random.shuffle(items_to_choose_from)
  items_picked = []
  #[item_name]; [class]; [weight]; [cost]; [resale value]

  #heuristic: the solution is done if you've used 90% of your money and 90% of your weight
  #this way you don't have to iterate through all the items

  total_cost = 0
  total_weight = 0


  for item in items_to_choose_from:
  	total_weight += item[2]
  	total_cost += item[3]
  	#item is too heavy / costs too much
  	if total_weight > P  or total_cost > M:
  		total_weight -= item[2]
  		total_cost -= item[3]
    #item puts knapsack in heuristic "good enough" spot, so exit loop
  	elif total_weight > 9 * P / 10 and total_cost > 9 * M / 10:
  		items_picked += [item]
  		break
    #just add item
  	else:
  		items_picked += [item]

  #assign fitness value
  #output 0101001100101001001010101

  return items_picked

def check_random_solution(P, M, N, C, items, constraints, file_num):
	chromosome_file_name = "population/problem" + file_num + "chromosome" + str(1) + ".p"
	chromosome = pickle.load( open( chromosome_file_name, "rb" ) )
	total_cost = 0
	total_weight = 0
	for item in chromosome:
		total_cost += item[3]
		total_weight += item[2]
	print("Total leftover money for problem " + file_num + "chromosome 1: " + str(M - total_cost) + "\n")
	print("Total leftover pounds for problem " + file_num + ": " + str(P - total_weight) + "\n")
	return chromosome




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
  parser.add_argument("mode", type=int, help="____.dongus")
  args = parser.parse_args()

  P, M, N, C, items, constraints = read_input(args.input_file)
  mode = args.mode
  items_chosen = solve(P, M, N, C, items, constraints, mode, args.input_file)
  write_output(args.output_file, items_chosen)