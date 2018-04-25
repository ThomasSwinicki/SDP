#script to shrink images to a quarter of their size
from random import randint
from cv2 import imread, imwrite, resize

def shrink_it(img_name):
	img = imread(img_name)
	img_name = img_name[:-4]

	#img = cv2.imread('IMG_7559.jpg')

	smaller = resize(img, (0,0), fx=0.25, fy=0.25)
	name    = 'images/image_small'+str(randint(100,999))+'.jpg'
	imwrite(name, smaller)
	return name
