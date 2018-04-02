import cv2
import numpy as np
import math
import argparse

img = cv2.imread("IMG_7596_small.jpg")
img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

red = img[250:300,300:400]
yellow = img[350:400,300:400]
green = img[440:490,300:400]
blue = img[520:570,300:400]
white = img[620:670,300:400]
colors = [red, yellow, green, blue, white]

for c in colors:
	cv2.imshow('ROI', c)
	cv2.waitKey(0)

width, height = 50,100 
vals = []
#make i a tenth of the larger edge of the ROI
for c in colors:
	for i in range(0,math.floor(width/10)):
                for j in range(0, math.floor(height/10)):
                        #to access HSV of an image use image[x][y][z], where x,y,z are the HSV values resepctively
                        vals[colors.index(c)].append([c[i*10][j*10][0], c[i*10][j*10][1], c[i*10][j*10][2]])

#print(vals)

#get min and max of each
colormins = [[360,360,360],[360,360,360],[360,360,360],[360,360,360],[360,360,360]]
colormaxs = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

for HSV in vals:
	for c in range(0,5):
        	for i in range(0,3):
                	if(HSV[c][i] < colormins[c][i]):
                        	colormins[c][i] = HSV[c][i]
                	if(HSV[i] > colormaxs[i]):
                        	colormaxs[c][i] = HSV[c][i]
print(colormins)
print(colormaxs)

