#sort the items according to class in ascending order
#sort the constraints horizontally in ascending order
#sort the constraints vertically in ascending order

#compare items within a class to check for superior items
#delete the inferior items

#compare classes to see if there are any superior classes

        #[P pounds]
        #[M dollars]
        #[N number of items]
        #[C number of constraints]

        #BufferedReader in = new BufferedReader(new FileReader("foo.in"));

        #put a file into buffered reader
        #create an arraylist of arraylists
        #each arraylist holds the strings of that class type
        #arraylist of arraylists numbered from 0 to N-1, since classes can be 0 to N-1
        #read a line
        #split based on semicolons
        #look at second parameter, the class
        #add that to arraylist of arraylists at the index = to its class #
        #now you have an array of arrays, with each array containing 1 class
        #print to new file
        #add in constraints later

#can't use relative path because script is not run from the same directory that sorter.py is in
unsorted_file = open('/home/miles/Downloads/CS170project/project_instances/problem1.in', 'r')
sorted_file = open('/home/miles/Downloads/CS170project/problem1sorted_file.in', 'w')
weight = unsorted_file.readline()
budget = unsorted_file.readline()
num_items = unsorted_file.readline()
num_constraints = unsorted_file.readline()

sorted_file.write(weight)
sorted_file.write(budget)
sorted_file.write(num_items)
sorted_file.write(num_constraints)

#convert these to ints for later use
num_items = int(num_items)
num_constraints = int(num_constraints)

#each list_i in classes holds all instances of class i
classes = [[] for i in range(num_items)]

#sort the items into their class
for index in range(num_items):
	#item_name, item_class, weight, cost, resale = unsorted_file.readline().split("; ")
	item = unsorted_file.readline()
	item_class = int(item.split("; ")[1])
	classes[item_class] += [item]

#sort all items in each class by value density
#for index in range(num_items):
#	class_i = classes[index]


#write the items into new file
for index in range(num_items):
	class_i_items = classes[index]
	for class_index in range(len(class_i_items)):
		sorted_file.write(class_i_items[class_index])

#sort the constraints and write to file
for index in range(num_constraints):
	string_constraint = unsorted_file.readline().split(", ")
	constraint = [int(i) for i in string_constraint]
	constraint.sort()
	sorted_file_string_constraint = ""
	for c in range(len(constraint)-1):
		sorted_file_string_constraint += str(constraint[c]) + ", "

	sorted_file_string_constraint += str(constraint[-1]) + "\n"
	sorted_file.write(sorted_file_string_constraint)

unsorted_file.close()
sorted_file.close()