import numpy as np
import cv2

img = cv2.imread('IMG_7509_small.jpg')

#for pixels in img, block off pixels into separate 50x50 blocks at about 40% into the x axis of the image (2/5 the max width)
#go down each block as see if any of the blocks contain one of our colors. If they do, they append that code to a text file (or python file) and go to the next block 

#list of boundaries for the colors in the following order: Blue, Green, Yellow, Orange, Gray, White
boundaries = [
	([100, 41, 21], [192, 169, 161]),
	([41, 68, 24], [109, 152, 109]),
	([70, 183, 120], [115, 253, 255]),
	([96, 169, 251], [110, 178, 255]),
	([93, 95, 96], [189, 205, 217]),
	([150, 170, 180], [255, 255, 255])
]

for (lower, upper) in boundaries:
	lower = np.array(lower, dtype='uint8')
	upper = np.array(upper, dtype='uint8')
	
	mask = cv2.inRange(img, lower, upper)
	output = cv2.bitwise_and(img, img, mask=mask)

	cv2.imshow("images", np.hstack([img, output]))
	cv2.waitKey(0)

