import cv2
from shapedetector import ShapeDetector
import numpy as np
import math
import argparse
import imutils

class Calibrator:
	
	#lowerhue = []
	#upperhue = []
	bounds = []

	def calibrate(self):
		img = cv2.imread("IMG_7694_small.jpg")
		#img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
		
		lower = np.array([0,0,0], dtype='uint8')
		upper = np.array([255,255,255], dtype='uint8')
		mask = cv2.inRange(img, lower, upper)
		output = cv2.bitwise_and(img, img, mask=mask)

		resized = imutils.resize(output, width=300)
		ratio = output.shape[0] / float(resized.shape[0])
		
		#tempg = cv2.cvtColor(resized, cv2.COLOR_HSV2RGB)
		gray = cv2.cvtColor(resized, cv2.COLOR_RGB2GRAY)
		blurred = cv2.GaussianBlur(gray, (5,5), 0)
		thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if imutils.is_cv2() else cnts[1]
		sd = ShapeDetector()

		img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

#		for c in cnts:
		c = cnts[0];
		shape = sd.detect(c)

		c = c.astype("float")
		c *= ratio
		c = c.astype("int")
		x,y,w,h = cv2.boundingRect(c)
		#print(str(x) + ", " + str(y) + ", " + str(w) + ", " + str(h) + "....")

		cv2.drawContours(output, [c], -1, (0,255,0), 2)
		#get roi of original image
		try:
			#cv2.imshow("img", img)
			#cv2.waitKey(0)
			#use for debuggin
			#cv2.imshow("Instruct", img[y:(y+h), x:(x+w)])
			#cv2.waitKey(0)
			allcolors = img[y:(y+h), x:(x+w)]
		except:
				print("Zero value")

		img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)	
		#every color is a fourth of the image
		cht = h/4
		#ues a quarter of the width for ROIs
		cwid = w/4
		vROI = cht / 4
		
		cht = int(cht)
		cwid = int(cwid)
		vROI = int(vROI) 		

		#image ROI are in [rows,columns] format => [y,x]
		red = allcolors[vROI:3*vROI, cwid: 3*cwid]
		yellow = allcolors[cht + vROI: cht + 3*vROI, cwid: 3*cwid]
		green = allcolors[2*cht + vROI: 2*cht + 3*vROI, cwid: 3*cwid]
		blue = allcolors[3*cht + vROI: 3*cht + 3*vROI, cwid: 3*cwid]
		#red = img[250:300,300:400]
		#yellow = img[350:400,300:400]
		#green = img[440:490,300:400]
		#blue = img[520:570,300:400]
		#white = img[620:670,300:400]
		#red = img[290:310,300:400]
		#yellow = img[380:400,300:400]
		#green = img[470:490,300:400]
		#blue = img[560:580,300:400]
		#white = img[650:670,300:400]	
		colors = [red, yellow, green, blue] #, white]

		#for debugging
		#for c in colors:
		#	cv2.imshow('ROI', c)
		#	cv2.waitKey(0)

		height, width= red.shape[:2]
		vals = [[] for i in range(5)]
		#make i a tenth of the larger edge of the ROI
		for c in range(len(colors)):
			for j in range(1,math.floor(width/10)):
				for i in range(1, math.floor(height/10)):
					#to access HSV of an image use image[x][y][z], where x,y,z are the HSV values resepctively
					vals[c].append((colors[c][i*10][j*10][0], colors[c][i*10][j*10][1], colors[c][i*10][j*10][2]))


		#get min and max of each
		colormins = [[360,360,360],[360,360,360],[360,360,360],[360,360,360],[360,360,360]]
		colormaxs = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

		#vals = [ [3-tuples of HSV vals of red], [3-tuples of HSV vals of yellow], [...green], [...blue], [...white] ]
		for HSVlist in vals:
			#using the 3-tuples of a color, HSV[0] is first tuple, HSV[0][0] is its hue, HSV[0][1] is its saturation, HSV[0][2] is its value
			colorindex = vals.index(HSVlist)
			for HSVvals in HSVlist:
				#now we are using each tuple in each list of tuples for each color
				#for i in range(3):
				#	if(HSVvals[i] > colormaxs[colorindex][i]):
				#		colormaxs[colorindex][i] = HSVvals[i]
				#	if(HSVvals[i] < colormins[colorindex][i]):
				#		colormins[colorindex][i] = HSVvals[i]
				for i in range(1):
					if(HSVvals[i] > colormaxs[colorindex][i]):
						colormaxs[colorindex][i] = HSVvals[i]
					if(HSVvals[i] < colormins[colorindex][i]):
						colormins[colorindex][i] = HSVvals[i]
				for i in range(1,3):
					colormaxs[colorindex][i] = 255
					colormins[colorindex][i] = 0

		#self.lowerhue = [colormins[0][0], colormins[1][0], colormins[2][0], colormins[3][0], colormins[4][0]]
		#self.upperhue = [colormaxs[0][0], colormaxs[1][0], colormaxs[2][0], colormaxs[3][0], colormaxs[4][0]]
		huemins = []
		huemaxs = []
		#for h in colormins:
		#	huemins.append(h[0]);
		#for h in colormaxs:
		#	huemaxs.append(h[0]);
		#print(huemins)
		#print(huemaxs)
		for i in range(4):
			self.bounds.append((colormins[i],colormaxs[i]))
			#self.bounds.append((huemins[i],huemaxs[i]))	

	def __init__(self):
		self.calibrate()


	def hueRange(self):
		return(self.bounds)
