import cv2
import numpy as np
import math

img = cv2.imread("IMG_7532_small.jpg");

imgROI = img[300:500, 300:500];

cv2.imshow('ROI', imgROI);
cv2.waitKey(0);

hsvimg = cv2.cvtColor(imgROI, cv2.COLOR_RGB2HSV);

width, height = hsvimg.shape[:2]
vals = []
#make i a tenth of the larger edge of the ROI
for i in range(0,math.floor(width/10)):
                for j in range(0, math.floor(height/10)):
                        #to access HSV of an image use image[x][y][z], where x,y,z are the HSV values resepctively
                        vals.append([hsvimg[i*10][j*10][0],hsvimg[i*10][j*10][1], hsvimg[i*10][j*10][2]])

#print(vals)

#get min and max of each
mins = [360,360,360]
maxs = [0, 0, 0]
for HSV in vals:
        for i in range(0,3):
                if(HSV[i] < mins[i]):
                        mins[i] = HSV[i]
                if(HSV[i] > maxs[i]):
                        maxs[i] = HSV[i]
print(mins)
print(maxs)

