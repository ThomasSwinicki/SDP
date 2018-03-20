import numpy as np
import cv2 

img1 = cv2.imread('IMG_5760.JPG')
img2 = cv2.imread('IMG_5761.JPG')
img3 = cv2.imread('IMG_5762.JPG')

#shrink images by a factor of 4
img1small = cv2.resize(img1, (0,0), fx = 0.25, fy = 0.25)
img2small = cv2.resize(img2, (0,0), fx = 0.25, fy = 0.25)
img3small = cv2.resize(img3, (0,0), fx = 0.25, fy = 0.25)

cv2.imwrite('IMG_5760_2.JPG', img1small)
cv2.imwrite('IMG_5761_2.JPG', img2small)
cv2.imwrite('IMG_5762_2.JPG', img3small)
