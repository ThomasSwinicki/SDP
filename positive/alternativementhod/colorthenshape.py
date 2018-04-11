from shapedetector import ShapeDetector
from calibrateHSV import Calibrator
import numpy as np
import cv2
import argparse
from operator import itemgetter
import imutils

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

#for HSV
imgin = cv2.imread(args["image"])
img = cv2.cvtColor(imgin, cv2.COLOR_RGB2HSV);

#for RGB
#img = cv2.imread(args["image"])

#boundaries are in the order of Red, Yellow, Green, Blue
calib = Calibrator()
boundaries = calib.hueRange()
print(boundaries)
boundaries[2][0][0] += 0;
boundaries[2][1][0] += -1;
#change the ranges for green to be RGB
boundaries[2] = ([41, 68, 24], [112,166,106])
print(boundaries);
#boundaries = [(220,250),(85,140),(40,70),(0,20),(65,115)]
#boundaries = [([115,100,195] , [120,190,230]),([89,0,0] , [94,255,255]),([42,0,0] , [47,255,255]),([5,0,0] ,[15,255,255]),([95,0,0],[110,255,255])]
#boundaries = [([110,0,0] , [120,255,255]),([89,0,0] , [94,255,255]),([42,0,0] , [47,255,255]),([5,0,0] ,[15,255,255]),([95,0,0],[110,255,255])]
#boundaries = [([110,0,50] , [120,255,255]),([89,0,50] , [94,255,255]),([42,0,50] , [47,255,255]),([5,0,50] ,[15,255,255]),([95,0,50],[110,255,255])]

#list of RGB (BGR in numpy)boundaries for the colors in the following order: Blue, Green, Yellow, Red, White
#boundaries = [
#        ([100, 41, 21], [192, 102, 70]),
#        ([41, 68, 24], [112,166,106]),
#        ([70, 183, 120], [115, 253, 255]),
#        ([29,39,140], [100,100,255]),
#        ([160, 180, 185], [255, 255, 255])
#]



#array for the number of times an instruction has been output to the text file, to keep track of which instructions have already been accounted for 
instructs = [] 
i = 0
abr = ['b','g','y','r','w']

for (lower, upper) in boundaries:
	lower = np.array(lower, dtype='uint8')
	upper = np.array(upper, dtype='uint8')

	if i != 2:
		mask = cv2.inRange(img, lower, upper)
		output = cv2.bitwise_and(img, img, mask=mask)
		cv2.imshow("output", output)
		cv2.waitKey(0)
	else:#use RGB for green
		tempimg = cv2.cvtColor(img, cv2.COLOR_HSV2RGB);
		mask = cv2.inRange(tempimg, lower, upper);
		output = cv2.bitwise_and(img, img, mask=mask)
	#shape detection
	resized = imutils.resize(output, width=300)
	ratio = output.shape[0] / float(resized.shape[0])

	#for HSV
	temp = cv2.cvtColor(resized, cv2.COLOR_HSV2RGB)
	gray = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
	
	if i==2:
		#for RGB
		gray = cv2.cvtColor(resized, cv2.COLOR_RGB2GRAY)
	blurred = cv2.GaussianBlur(gray, (5,5), 0)
	thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
	
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	sd = ShapeDetector()
	
	for c in cnts:
		shape = sd.detect(c)
		
		c = c.astype("float")
		c *= ratio
		c = c.astype("int")
		x,y,w,h = cv2.boundingRect(c)
		#print(str(x) + ", " + str(y) + ", " + str(w) + ", " + str(h) + "....")
		
		cv2.drawContours(output, [c], -1, (0,255,0), 2)
		instructs.append((abr[i], y))
		#get roi of original image
		try:
			#cv2.imshow("img", img)
			#cv2.waitKey(0)
			cv2.imshow("Instruct", img[y:(y+h), x:(x+w)])
			cv2.waitKey(0)
		except:
			print("Zero value")
		#cv2.imshow("Image", output)
		#cv2.waitKey(0)
	#end shape detetion script
	
	cv2.imshow("images", np.hstack([img, output]))
	cv2.waitKey(0)
	i += 1
print(instructs)
instructs.sort(key=itemgetter(1))
print(instructs)

code = open("codetest.txt", 'w')
for lines in instructs:
	if(lines[0] == 'b'):
		code.write('forward command\n')
	elif(lines[0] == 'g'):
		code.write('turn left\n')
	elif(lines[0] == 'y'):
		code.write('preliniary for\n')
	elif(lines[0] == 'r'):
		code.write('turn right\n')
	else:
		code.write('number\n')
