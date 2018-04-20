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
#print(shrinkcommand)
subprocess.Popen(shrinkcommand.split(), stdout=subprocess.PIPE)
args["image"] = args["image"].replace(".jpg", "_small.jpg")
#print(args["image"])
#for HSV
time.sleep(0.5)
imgin = cv2.imread(args["image"])
img = cv2.cvtColor(imgin, cv2.COLOR_RGB2HSV);

#for RGB
#img = cv2.imread(args["image"])

#if scheme is 0, green is using RGB (for debugging)
scheme = 1;

#boundaries are in the order of Red, Yellow, Green, Blue
calib = Calibrator()
boundaries = calib.hueRange()
boundaries = [i for i in range(4)]
#print(boundaries)
#boundaries[2][0][0] += 0;
#boundaries[2][1][0] += -1;
#change the ranges for green to be RGB
boundaries[3] = ([114,20,20], [120,255,255])
boundaries[1] = ([90,80,80], [99,255,255])

if(scheme == 0):
	#RGB green
	boundaries[2] = ([41, 68, 24], [112,166,106])
else:
	#HSVgreen
	boundaries[2] = ([35,10,10], [60,255,255])

boundaries[0] = ([7,20,20], [14,255,255])
#print(boundaries);
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
inst = 0
#abr = ['b','g','y','r','w']
abr = ['b','y','g','r']
instrwidth = 0
instrheight = 0
for (lower, upper) in boundaries:
	lower = np.array(lower, dtype='uint8')
	upper = np.array(upper, dtype='uint8')

	if i != 2:
		mask = cv2.inRange(img, lower, upper)
		output = cv2.bitwise_and(img, img, mask=mask)
		cv2.imshow("output", output)
		cv2.waitKey(0)
	else:#use RGB for green
		if(scheme == 0):
			tempimg = cv2.cvtColor(img, cv2.COLOR_HSV2RGB);
			mask = cv2.inRange(tempimg, lower, upper);
		else:
			mask = cv2.inRange(img,lower,upper);
		output = cv2.bitwise_and(img, img, mask=mask)
		cv2.imshow("output", output)
		cv2.waitKey(0)
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
	if(abr[i] != 'r'):
		thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
	else:
		thresh = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY)[1]
	cv2.imshow("thresh", thresh)
	cv2.waitKey(0)

	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	sd = ShapeDetector()
	ccount = 0	
	print("working on " + str(abr[i]) +" instructions")
	for c in cnts:
		shape = sd.detect(c)
		
		c = c.astype("float")
		c *= ratio
		c = c.astype("int")
		x,y,w,h = cv2.boundingRect(c)
		#print(str(x) + ", " + str(y) + ", " + str(w) + ", " + str(h) + "....")
		
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
		print("Number for instruction: " + str(instructs[inst][3]))
		if(abr[i] == 'y'):
			instructs[inst+1][3] = x
			inst +=2
		else:
			inst += 1
		#except:
			#print("writing tiff or number detection error")
		try:
			cv2.imshow("number", numROI)
			cv2.waitKey(0)
		except:
			print("pixel detected too far show")
		#get roi of original image
		try:
			#cv2.imshow("img", img)
			#cv2.waitKey(0)
			cv2.imshow("Instruct", img[y:(y+h), x:(x+w)])
			cv2.waitKey(0)
		except:
			print("Zero value for instruct")
		#cv2.imshow("Image", output)
		#cv2.waitKey(0)
		ccount += 1
	#end shape detetion script
	print("contour count: " + str(ccount))
	cv2.imshow("images", np.hstack([imgin, cv2.cvtColor(output,cv2.COLOR_HSV2RGB)]))
	cv2.waitKey(0)
	i += 1
print(instructs)
instructs.sort(key=itemgetter(1))
print(instructs)
inloopcount = 0

code = open("codetest.txt", 'w')
codestring = ''
for lines in instructs:
	if(lines[0] == 'b'):
		code.write('f,' + str(lines[3]) + ' ')
		codestring += 'f,' + str(lines[3]) + ' '
	elif(lines[0] == 'g'):
		code.write('l,' + str(lines[3]) + ' ')
		codestring += 'l,' + str(lines[3]) + ' '
	elif(lines[0] == 'y' and lines[2] == 0):
		#beginning of for loop
		code.write('(,' + str(lines[3]) + ' ')
		codestring += '(,' + str(lines[3]) + ' '
	elif(lines[0] == 'y' and lines[2] == 1):
		#end of for loop
		code.write('),' + str(lines[3]) + ' ')
		codestring += '),' + str(lines[3]) + ' '
	elif(lines[0] == 'r'):
		code.write('r,' + str(lines[3]) + ' ')
		codestring += 'r,' + str(lines[3]) + ' '
	else:
		code.write('number\n')
print(codestring)

