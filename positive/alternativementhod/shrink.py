#script to shrink images to a quarter of their size
import numpy as np
import cv2
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

img = cv2.imread(args["image"])
args["image"] = args["image"][:-4]

height,width = img.shape[:2]
#img = cv2.imread('IMG_7559.jpg')

if width == 3024 and height == 4032: #dimensions of Kelly's and Michelle's phone
	smaller = cv2.resize(img, (0,0), fx=0.25, fy=0.25)
elif height == 5312 and width == 2988: #dimensions of Tom's phone
	print("toms")	
elif height == 600 and width ==470: #dimensions from flask
	print("flask")
cv2.imwrite(args["image"]+'_small.jpg', smaller)
