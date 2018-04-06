import numpy as np
import cv2
import argparse

#img = cv2.imread('IMG_7527_small.jpg')

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="path to image")
args = vars(ap.parse_args())

img = cv2.imread(args["image"])

#for pixels in img, block off pixels into separate 50x50 blocks at about 40% into the x axis of the image (2/5 the max width)
#go down each block as see if any of the blocks contain one of our colors. If they do, they append that code to a text file (or python file) and go to the next block 

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

	cv2.imshow("images", np.hstack([img, output]))
	cv2.waitKey(0)

