#script to run classifier of forward instruction on test images specified as img
import numpy as np
import cv2

forward_cascade = cv2.CascadeClassifier('cascadedata/cascade.xml')

img = cv2.imread('../IMG_7147.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

forward = forward_cascade.detectMultiScale(gray, 1.3, 5)

for (x,y,w,h) in forward:
        cv2.rectangle(img[x,y], (x+w, y+h), (255,0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

cv2.imshow('img',img)
cvw.waitKey(0)
cv2.destroyAllWindows()

