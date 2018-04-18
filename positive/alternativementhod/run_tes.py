import subprocess

# input_img = argv[1]
def run_tesseract(input_img):
	command   = 'tesseract {} stdout --psm 7 digits'.format(input_img)

	proc = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE)
	s    = proc.communicate()[0]
	num  = ''

	for val in list(str(s)):
		if val.isdigit():
			num += val			
	
	return num
