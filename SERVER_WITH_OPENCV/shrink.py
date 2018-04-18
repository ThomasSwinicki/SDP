#script to shrink images to a quarter of their size
import numpy as np
import cv2
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

img = cv2.imread(args["image"])
args["image"] = args["image"][:-4]

#img = cv2.imread('IMG_7559.jpg')

smaller = cv2.resize(img, (0,0), fx=0.25, fy=0.25)

cv2.imwrite('image_small.jpg', smaller)
