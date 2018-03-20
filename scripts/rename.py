import glob
import os

for f in glob.glob('Copy*'):
	new_filename = f.replace("Copy of ", "")
	os.rename(f, new_filename)
