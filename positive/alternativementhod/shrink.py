#script to shrink images to a quarter of their size
import numpy as np
import cv2

img = cv2.imread('IMG_7504.jpg')

smaller = cv2.resize(img, (0,0), fx=0.25, fy=0.25)

cv2.imwrite('IMG_7504_small.jpg', smaller)
