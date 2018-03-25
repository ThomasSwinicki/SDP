import numpy as np
import cv2
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
args = vars(ap.parse_args())

img = cv2.imread(args["image"])

cv2.imshow("block", img[332:381, 269:310])
cv2.waitKey(0)
