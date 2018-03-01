import numpy as np
import xlrd
import pandas
import math

names = pandas.read_excel('Coordinates.xlsx')

#value of names.columns:
#Index(['Image Name', 'Instr', 'Folder Name', 'Top Left', 'Unnamed: 4', 'Width',
#       'Unnamed: 6', 'Height', 'Unnamed: 8', 'OpenCV Name\n(x y width height)',
#       'Notes'],
#      dtype='object')

for i in range(1,len(names['Image Name'].values)):
	filename = "pos_" + names['Instr'][i] + ".info"
	while(names['Image Name'][i] != None):
		with open(filename , 'a') as out:
			print(r"OpenCV Name\n(x y width height)")
			out.write(names['Image Name'][i] + names[r"OpenCV Name\n(x y width height)"][i] + '\n')
