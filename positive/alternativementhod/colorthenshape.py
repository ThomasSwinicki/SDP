from shapedetector import ShapeDetector
import numpy as np
import cv2
import argparse
import imutils

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

img = cv2.imread(args["image"])

#list of boundaries for the colors in the following order: Blue, Green, Yellow, Red, Gray, White
boundaries = [
        ([100, 41, 21], [192, 102, 70]),
        ([41, 68, 24], [112,166,106]),
        ([70, 183, 120], [115, 253, 255]),
        ([29,39,140], [100,100,255]),
        ([93, 95, 96], [149, 169, 179]),
        ([160, 180, 185], [255, 255, 255])
]

#array for the number of times an instruction has been output to the text file, to keep track of which instructions have already been accounted for 
numinstructs = [0,0,0,0,0,0]

for (lower, upper) in boundaries:
	lower = np.array(lower, dtype='uint8')
	upper = np.array(upper, dtype='uint8')

	mask = cv2.inRange(img, lower, upper)
	output = cv2.bitwise_and(img, img, mask=mask)
	
	#shape detection
	resized = imutils.resize(output, width=300)
	ratio = output.shape[0] / float(resized.shape[0])

	gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
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
        	cv2.drawContours(output, [c], -1, (0,255,0), 2)
    	
        	#cv2.imshow("Image", output)
        	#cv2.waitKey(0)
	#end shape detetion script
	
	cv2.imshow("images", np.hstack([img, output]))
	cv2.waitKey(0)

