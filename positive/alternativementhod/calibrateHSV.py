import cv2
import numpy as np
import math
import argparse

img = cv2.imread("IMG_7596_small.jpg")
img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

#image ROI are in [rows,columns] format => [y,x]
red = img[250:300,300:400]
yellow = img[350:400,300:400]
green = img[440:490,300:400]
blue = img[520:570,300:400]
white = img[620:670,300:400]
colors = [red, yellow, green, blue, white]

for c in colors:
	cv2.imshow('ROI', c)
	cv2.waitKey(0)

height, width= red.shape[:2]
print(width)
print(height) 
vals = [[] for i in range(5)]
#make i a tenth of the larger edge of the ROI
for c in range(len(colors)):
	for j in range(1,math.floor(width/10)):
		for i in range(1, math.floor(height/10)):
			#to access HSV of an image use image[x][y][z], where x,y,z are the HSV values resepctively
			vals[c].append((colors[c][i*10][j*10][0], colors[c][i*10][j*10][1], colors[c][i*10][j*10][2]))

#print(vals[0])
#print('......\n')
#print(vals[1])
#print('......\n')
#print(vals[2])
#print('......\n')
#print(vals[3])
#print('......\n')
#print(vals[4])
#print('......\n')

#get min and max of each
colormins = [[360,360,360],[360,360,360],[360,360,360],[360,360,360],[360,360,360]]
colormaxs = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

#for HSV in vals:
#	j = 0
#	for c in range(len(HSV)):
#		for i in range(0,3):
#			if(HSV[c][i] < colormins[j][i]):
#				colormins[j][i] = HSV[c][i]
#			if(HSV[c][i] > colormaxs[j][i]):
#				colormaxs[j][i] = HSV[c][i]
#	j+=1

#vals = [ [3-tuples of HSV vals of red], [3-tuples of HSV vals of yellow], [...green], [...blue], [...white] ]
for HSVlist in vals:
	#using the 3-tuples of a color, HSV[0] is first tuple, HSV[0][0] is its hue, HSV[0][1] is its saturation, HSV[0][2] is its value
	colorindex = vals.index(HSVlist)
	for HSVvals in HSVlist:
		#now we are using each tuple in each list of tuples for each color
		for i in range(3):
			if(HSVvals[i] > colormaxs[colorindex][i]):
				colormaxs[colorindex][i] = HSVvals[i]
			if(HSVvals[i] < colormins[colorindex][i]):
				colormins[colorindex][i] = HSVvals[i]

print(colormins)
print(colormaxs)
lowerhue = [colormins[0][0], colormins[1][0], colormins[2][0], colormins[3][0], colormins[4][0]]
upperhue = [colormaxs[0][0], colormaxs[1][0], colormaxs[2][0], colormaxs[3][0], colormaxs[4][0]]
print(lowerhue)
print(upperhue)
	


def hueRange:
	return(lowerhue,upperhue)
