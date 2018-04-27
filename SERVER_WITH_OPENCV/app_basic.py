import os, subprocess, random
from expand_for_loop import run_commands
from send2robot      import send_commands
from flask import Flask, render_template, request

__author__ = 'ibininja'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
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
		
		send_commands(run_commands(result))

	text = request.form['text']	
	print(text)

	return render_template("upload.html")

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=4555, debug=True)
