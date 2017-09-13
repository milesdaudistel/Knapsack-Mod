
unoptimized = open('/home/miles/Downloads/CS170project/problem1sorted_file.in', 'r')
optimized = open('/home/miles/Downloads/CS170project/problem1optimized.in', 'w')

weight = unoptimized.readline()
budget = unoptimized.readline()
num_items = unoptimized.readline()
num_constraints = unoptimized.readline()

optimized.write(weight)
optimized.write(budget)
optimized.write(num_items)
optimized.write(num_constraints)

#convert these to ints for later use
num_items = int(num_items)
num_constraints = int(num_constraints)


classes = [[] for i in range(num_items)]
for i in range(27):
	item = unoptimized.readline().split("; ")
	item[1] = int(item[1])
	item[2] = float(item[2])
	item[3] = float(item[3])
	item[4] = float(item[4])
	item = tuple(item)
	classes[i] += item
	#print(type(classes[i][4]))



for class_i in classes:
	print(class_i[0])
	class_i = sorted(class_i, key=lambda x: (x[4]-x[3])/x[2])
	print(class_i)
	for item in class_i:
		optimized.write(str(item[0]) + ", " + str(item[1]) + ", " + str(item[2]) + ", " + str(item[3]) + ", " + str(item[4]) + "\n")


'''
#each list_i in classes holds all instances of class i
classes = [[] for i in range(num_items)]

#[item_name]; [class]; [weight]; [cost]; [resale value]

for index in range(num_items):
	#0: item_name, 1: item_class, 2: weight, 3: cost, 4: resale = unoptimized.readline().split("; ")
	item = unoptimized.readline().split("; ")
	##item_name, item_class, weight, cost, resale are now floats instead of strings
	item[1] = int(item[1])
	item[2] = float(item[2])
	item[3] = float(item[3])
	item[4] = float(item[4])
	
	#item[1] = item class
	classes[item[1]] += [item]

#sort in ascending order by (resale-cost) / weight
for class_i in classes:
	#sort each class by its value density
	#class_i = sorted(class_i, key=lambda x: (x[4]-x[3])/x[2])
	for item in class_i:
		#convert all parts of the item back into string
		for attribute in range(len(item)):
			item[attribute] = str(item[attribute])
		#item = item[0] + ", " + item[1] + ", " + item[2] + ", " + item[3] + ", " + item[4]
		optimized.write(item[0] + ", " + item[1] + ", " + item[2] + ", " + item[3] + ", " + item[4]) + "\n"
'''
unoptimized.close()
optimized.close()

