import subprocess
from time import sleep

def switch(cmd):
	switcher = {
		'f': forward,
		'r': turn_right,
		'l': turn_left
	}
	return switcher[cmd]

def forward(dist):
	dist_convert = lambda dist: 50 if dist == 1 else int(dist*50)
	dist = dist_convert(dist)

	instruction = """#!/usr/bin/env bash~
			
			 export rm=/sys/class/tacho-motor/motor1~
			 export lm=/sys/class/tacho-motor/motor0~
			
			 echo reset > $rm/command~ 
			 echo reset > $lm/command~

			 echo coast > $rm/stop_action~
			 echo coast > $lm/stop_action~

			 echo 120   > $rm/speed_sp~
			 echo 120   > $lm/speed_sp~

			 echo {}    > $rm/position_sp~
			 echo {}    > $lm/position_sp~

			 echo run-to-rel-pos > $rm/command~
			 echo run-to-rel-pos > $lm/command~""".format(dist,dist).replace('\t','').replace('\n','').replace('~','\n')

	return instruction

def turn_right(degree):
	turn_convert = lambda degree: int((degree*268)/90)
	degree       = turn_convert(degree)

	instruction = """#!/usr/bin/env bash~

			 export rm=/sys/class/tacho-motor/motor1~
			 export lm=/sys/class/tacho-motor/motor0~
			 
			 echo reset > $rm/command~
			 echo reset > $lm/command~

			 echo brake > $rm/stop_action~
			 echo brake > $lm/stop_action~

			 echo -120  > $rm/speed_sp~
			 echo 120   > $lm/speed_sp~

			 echo {}    > $rm/position_sp~
			 echo {}    > $lm/position_sp~

			 echo run-to-rel-pos > $rm/command~
			 echo run-to-rel-pos > $lm/command~""".format(-degree,degree).replace('\t','').replace('\n','').replace('~','\n')

	return instruction

def turn_left(degree):
	turn_convert = lambda degree: int((degree*268)/90)
	degree	     = turn_convert(degree)

	instruction = """#!/usr/bin/env bash~

			 export rm=/sys/class/tacho-motor/motor1~
			 export lm=/sys/class/tacho-motor/motor0~

			 echo reset > $rm/command~
			 echo reset > $lm/command~
			
			 echo brake > $rm/stop_action~
			 echo brake > $lm/stop_action~
			
			 echo 120   > $rm/speed_sp~
			 echo -120  > $lm/speed_sp~

			 echo {}    > $rm/position_sp~
			 echo {}    > $lm/position_sp~

			 echo run-to-rel-pos > $rm/command~
			 echo run-to-rel-pos > $lm/command~""".format(degree,-degree).replace('\t','').replace('\n','').replace('~','\n')

	return instruction

def send_commands(final_commands):
	from math import ceil	

	for command,arg in final_commands:
		wait = ceil(arg*1.25) if arg < 10 else ceil(arg/30)

		temp_file = open('temp.sh', 'w')
		temp_file.write(switch(command)(arg))
		temp_file.close()

		proc = subprocess.Popen('cat temp.sh | nc localhost 5900', shell=True)
		proc.communicate()
		sleep(wait)
	
