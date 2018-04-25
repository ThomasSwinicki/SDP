from shapedetector import ShapeDetector
#from calibrateHSV import Calibrator
from run_tes  import run_tesseract
from shrink   import shrink_it
from numpy    import array
from cv2      import imread, cvtColor, GaussianBlur, threshold, findContours, boundingRect, imwrite, inRange, bitwise_and
from cv2      import COLOR_RGB2HSV, COLOR_HSV2RGB, COLOR_RGB2GRAY, THRESH_BINARY, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE
from argparse import ArgumentParser
from operator import itemgetter
from imutils  import resize, is_cv2

ap = ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

#shrinkcommand = "python3 shrink.py --image " + args["image"]
#subprocess.Popen(shrinkcommand.split(), stdout=subprocess.PIPE)
# args["image"] = args["image"].replace(".jpg", "_small.jpg")
# for HSV
img_name = shrink_it(args['image'])
imgin    = imread(img_name)
img      = cvtColor(imgin, COLOR_RGB2HSV);

#boundaries are in the order of Blue, Yellow, Green, Red
boundaries = [i for i in range(4)]
boundaries[3] = ([117,40,40], [120,255,255])
boundaries[1] = ([90,80,80], [99,255,255])
boundaries[2] = ([35,20,20], [60,255,255])
boundaries[0] = ([7,20,20], [13,255,255])

#array for the number of times an instruction has been output to the text file, to keep track of which instructions have already been accounted for 
instructs = [] 
i = 0
inst = 0
abr = ['b','y','g','r']
instrwidth = 0
instrheight = 0
for (lower, upper) in boundaries:
	lower = array(lower, dtype='uint8')
	upper = array(upper, dtype='uint8')

	mask = inRange(img, lower, upper)
	output = bitwise_and(img, img, mask=mask)

	#shape detection
	resized = resize(output, width=300)
	ratio = output.shape[0] / float(resized.shape[0])

	#imshow("output", cvtColor(resized, cv2.COLOR_HSV2RGB))
	#waitKey(0)
	#for HSV
	temp = cvtColor(resized, COLOR_HSV2RGB)
	gray = cvtColor(temp, COLOR_RGB2GRAY)
	
	blurred = GaussianBlur(gray, (5,5), 0)
	if(abr[i] != 'r'):
		thresh = threshold(blurred, 60, 255, THRESH_BINARY)[1]
	else:
		thresh = threshold(blurred, 40, 255, THRESH_BINARY)[1]
	#imshow("thresh", thresh);
	#waitKey(0);

	cnts = findContours(thresh.copy(), RETR_EXTERNAL,
        CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if is_cv2() else cnts[1]
	sd = ShapeDetector()
	ccount = 0	
	for c in cnts:
		shape = sd.detect(c)
		c = c.astype("float")
		c *= ratio
		c = c.astype("int")
		x,y,w,h = boundingRect(c)
		print(abr[i] + " width : " + str(w))
		if(w < 30):
			continue
		
		#drawContours(output, [c], -1, (0,255,0), 2)
		instructs.append([abr[i], y, 0, 0])
		if(abr[i] == 'y'):
			instructs.append(['y', y+h, 1, ''])	
		if(abr[i] != 'y'):
			instrwidth = w
			instrheight = h		
			try:
				numROI = imgin[y+5: y + h-5, x+w+5: x+w+int(w/2)+20]
				#imshow("num", numROI)
				#waitKey(0)
			except:
				print("floating point exception on numROI")
		elif(abr[i] == 'y'):
			numROI = imgin[y+5: y+instrheight-5, x+w+5: x+w+int(instrwidth/2) - 5 + 20 ]
			#imshow("num", numROI)
			#waitKey(0)

		#try:
		imwrite("ROI.tiff", numROI)
		x = run_tesseract('ROI.tiff')
		numROI = cvtColor(numROI, COLOR_RGB2GRAY)
		#imshow("number", numROI)
		#waitKey(0)
		thresh_val = 50
		while (x == '' and thresh_val < 255):
			tmpROI = GaussianBlur(numROI, (5,5), 0)
			tmpROI = threshold(tmpROI, thresh_val, 255, THRESH_BINARY)[1]
			#imshow("thresh num", tmpROI)
			#waitKey(0)
			imwrite("ROI.tiff", tmpROI)
			x = run_tesseract('ROI.tiff')
			thresh_val += 25
			print('Current thresh value: {}'.format(thresh_val))

		if int(x) > 180:
			print('found number greater than 180: {}'.format(x))
			tmp = list(x)[::-1]
			try:
				tmp.remove('1')
			except:
				pass
			x = ''.join(tmp[::-1])

		instructs[inst][3] = x
		if(abr[i] == 'y'):
			instructs[inst+1][3] = x
			inst +=2
		else:
			inst += 1
		ccount += 1
	#end shape detetion script
	i += 1
instructs.sort(key=itemgetter(1))
inloopcount = 0

codestring = ''
for lines in instructs:
	if(lines[0] == 'b'):
		codestring += 'f,' + str(lines[3]) + ' '
	elif(lines[0] == 'g'):
		codestring += 'l,' + str(lines[3]) + ' '
	elif(lines[0] == 'y' and lines[2] == 0):
		#beginning of for loop
		codestring += '(,' + str(lines[3]) + ' '
	elif(lines[0] == 'y' and lines[2] == 1):
		#end of for loop
		codestring += '),' + str(lines[3]) + ' '
	elif(lines[0] == 'r'):
		codestring += 'r,' + str(lines[3]) + ' '
print(codestring)

