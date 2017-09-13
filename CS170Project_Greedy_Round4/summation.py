import pickle
total_profit_file = open('/home/miles/Downloads/CS170Project_Greedy_Round2/sum.out', 'w')
for i in range(1, 21):
	stri = str(i)
	problem_i_profit_file = "output/total_profit" + stri + ".p"
	problem_i_profit = pickle.load( open( problem_i_profit_file, "rb" ) )
	total_profit_file.write("Problem " + stri + ": " + str(problem_i_profit) + "\n")