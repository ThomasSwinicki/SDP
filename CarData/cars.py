cars = open("cars.info",'w')

for i in range(0,550):
	cars.write("positive/pos-" + str(i) + ".pgm 1 0 0 100 40 \n")
cars.close()
