from cv2 import arcLength, approxPolyDP

class ShapeDetector:
	def __init__(self):
		pass
		
	#only need to detect a rectangle or a 8-sided poly (for loop) for this project
	def detect(self, c):
		peri = arcLength(c,True)
		approx = approxPolyDP(c, 0.04*peri, True)
		if len(approx) == 4:
			shape = "instruction"
		else:
			shape = "for loop"	
