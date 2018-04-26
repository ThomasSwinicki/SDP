import os, subprocess, random
from flask import Flask, render_template, request

__author__ = 'ibininja'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def result_to_file(result):
	temp_file = open('temp.sh', 'w')
	temp_file.write('#!/usr/bin/env bash\n')
	temp_file.write("python3 robot.py '{}'\n".format(result))
	temp_file.close()
	return 'cat temp.sh | nc localhost 5900'

@app.route("/")
def index():
	return render_template("upload.html")

@app.route('/', methods=['POST'])
def my_form_post():
	text = request.form['text']
	result = text.lower()
	print('Result: {}'.format(result))

	proc = subprocess.Popen(result_to_file(result), shell=True)
	proc.communicate()

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
		result  = proc.communicate()[0].decode('utf-8').strip()
		print('Result: {}'.format(result))
		
		proc    = subprocess.Popen(result_to_file(result), shell=True)
		proc.communicate()
		# os.system('rm -vrf ' + destination)
	
	text = request.form['text']	
	print(text)

	return render_template("upload.html")

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=4555, debug=True)
