import numpy as np
import cv2

car_cascade = cv2.CascadeClassifier('data/cascade.xml')

img = cv2.imread('../TestImages/test-0.pgm')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cars = car_cascade.detectMultiScale(gray, 1.3, 5)

for (x,y,w,h) in cars:
        cv2.rectangle(img[x,y], (x+w, y+h), (255,0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

cv2.imshow('img',img)
cvw.waitKey(0)
cv2.destroyAllWindows()

