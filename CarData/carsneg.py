neg = open("bg.txt",'w')

for i in range(0,500):
	neg.write("negative/neg-" + str(i) + ".pgm\n")
neg.close()
