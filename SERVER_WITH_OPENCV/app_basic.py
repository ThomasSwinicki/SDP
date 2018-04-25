import os, subprocess, random
from flask import Flask, render_template, request

__author__ = 'ibininja'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
	return render_template("upload.html")

@app.route('/', methods=['POST'])
def my_form_post():
	text = request.form['text']
	processed_text = text.upper()
	command = "echo \"python3 robot.py '"+text+"'\" | ssh -T robot@ev3dev.local"
	print(processed_text)
	os.system('echo ' + processed_text)

	return render_template("upload.html")

@app.route("/upload", methods=['POST'])
def upload():
	target = os.path.join(APP_ROOT, 'images/')
	print(target)

	if not os.path.isdir(target):
		os.mkdir(target)
		
	for file in request.files.getlist("file"):
		print(file)
		filename = 'image'+str(random.randint(100,999))+'.jpg'
		print('filename = {}'.format(filename))
		destination = "/".join([target, filename])
		print(destination)
		file.save(destination)

		print('destination = {}'.format(destination))
		command = 'python extract.py --image ' + destination
		proc    = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		result  = proc.communicate()[0].decode('utf-8')
		print('Result: {}'.format(result))
		# os.system('rm -vrf ' + destination)
	
	text = request.form['text']	
	print(text)

	return render_template("upload.html")

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=4555, debug=True)
