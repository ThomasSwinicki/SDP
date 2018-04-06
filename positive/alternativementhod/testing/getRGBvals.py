import cv2
import numpy as np
import math

img = cv2.imread("IMG_7532_small.jpg");

imgROI = img[0:100, 0:100];

cv2.imshow('ROI', imgROI);
cv2.waitKey(0);

width, height = imgROI.shape[:2]
vals = []
#make i a tenth of the larger edge of the ROI
for i in range(0,math.floor(width/10)):
		for j in range(0, math.floor(height/10)):
			#to acess RGB of an image use image[x][y][z] where z is the R,G, or B (0,1,2)
			vals.append([imgROI[i*10][j*10][0],imgROI[i*10][j*10][1], imgROI[i*10][j*10][2]])

print(vals)

#get min and max of each
mins = [255,255,255]
maxs = [0, 0, 0]
for RGB in vals:
	for i in range(0,3):	
		if(RGB[i] < mins[i]):
			mins[i] = RGB[i]
		if(RGB[i] > maxs[i]):
			maxs[i] = RGB[i]
print(mins)
print(maxs)
