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

i = 0
while(i < len(names['Image Name'])):
	filename = "pos_" + str(names['Instr'][i]) + ".info"
	if(filename != "pos_nan.info" and str(names['Image Name'][i]) != 'nan'):
		with open(filename , 'a') as out:
			out.write(str(names['Image Name'][i]) + " 1 " + str(names[r"OpenCV Name(x y width height)"][i]) + '\n')
	i+=1
