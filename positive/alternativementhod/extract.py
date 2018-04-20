from shapedetector import ShapeDetector
from calibrateHSV import Calibrator
from run_tes import run_tesseract
import numpy as np
import cv2
import argparse
from operator import itemgetter
import imutils
import subprocess
import time

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

shrinkcommand = "python3 shrink.py --image " + args["image"]
subprocess.Popen(shrinkcommand.split(), stdout=subprocess.PIPE)
args["image"] = args["image"].replace(".jpg", "_small.jpg")
#for HSV
time.sleep(0.5)
imgin = cv2.imread(args["image"])
img = cv2.cvtColor(imgin, cv2.COLOR_RGB2HSV);

#boundaries are in the order of Red, Yellow, Green, Blue
boundaries = [i for i in range(4)]
boundaries[3] = ([114,20,20], [120,255,255])
boundaries[1] = ([90,80,80], [99,255,255])
boundaries[2] = ([35,10,10], [60,255,255])
boundaries[0] = ([7,20,20], [14,255,255])

#array for the number of times an instruction has been output to the text file, to keep track of which instructions have already been accounted for 
instructs = [] 
i = 0
inst = 0
abr = ['b','y','g','r']
instrwidth = 0
instrheight = 0
for (lower, upper) in boundaries:
	lower = np.array(lower, dtype='uint8')
	upper = np.array(upper, dtype='uint8')

	mask = cv2.inRange(img, lower, upper)
	output = cv2.bitwise_and(img, img, mask=mask)

	#shape detection
	resized = imutils.resize(output, width=300)
	ratio = output.shape[0] / float(resized.shape[0])

	#for HSV
	temp = cv2.cvtColor(resized, cv2.COLOR_HSV2RGB)
	gray = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
	
	blurred = cv2.GaussianBlur(gray, (5,5), 0)
	if(abr[i] != 'r'):
		thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
	else:
		thresh = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY)[1]

	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	sd = ShapeDetector()
	ccount = 0	
	for c in cnts:
		shape = sd.detect(c)
		
		c = c.astype("float")
		c *= ratio
		c = c.astype("int")
		x,y,w,h = cv2.boundingRect(c)
		
		cv2.drawContours(output, [c], -1, (0,255,0), 2)
		instructs.append([abr[i], y, 0, 0])
		if(abr[i] == 'y'):
			instructs.append(['y', y+h, 1, ''])	
		if(abr[i] != 'y'):
			instrwidth = w
			instrheight = h		
			try:
				numROI = imgin[y+5: y + h-5, x+w+5: x+w+int(w/2)]
			except:
				print("floating point exception on numROI")
		elif(abr[i] == 'y'):
			numROI = imgin[y+5: y+instrheight-5, x+w+5: x+w+int(instrwidth/2) - 5 ]
		#try:
		cv2.imwrite("ROI.tiff", numROI)
		x = run_tesseract('ROI.tiff')
		instructs[inst][3] = x
		if(abr[i] == 'y'):
			instructs[inst+1][3] = x
			inst +=2
		else:
			inst += 1
		ccount += 1
	#end shape detetion script
	i += 1
instructs.sort(key=itemgetter(1))
inloopcount = 0

codestring = ''
for lines in instructs:
	if(lines[0] == 'b'):
		codestring += 'f,' + str(lines[3]) + ' '
	elif(lines[0] == 'g'):
		codestring += 'l,' + str(lines[3]) + ' '
	elif(lines[0] == 'y' and lines[2] == 0):
		#beginning of for loop
		codestring += '(,' + str(lines[3]) + ' '
	elif(lines[0] == 'y' and lines[2] == 1):
		#end of for loop
		codestring += '),' + str(lines[3]) + ' '
	elif(lines[0] == 'r'):
		codestring += 'r,' + str(lines[3]) + ' '
print(codestring)

