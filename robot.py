#!/usr/bin/env python3
from sys import argv
import time
import ev3dev.ev3 as ev3

lm = ev3.Motor("outA")
rm = ev3.Motor("outD")

def forward (duration):
	t = float(dist_convert(duration))
	#s = int(speed)
	lm.reset()
	rm.reset()
	lm.run_to_rel_pos(position_sp = t*1000, speed_sp = 120, stop_action = "coast")
	rm.run_to_rel_pos(position_sp = t*1000, speed_sp = 120, stop_action = "coast")
	lm.wait_while('running') 
	rm.wait_while('running')
	time.sleep(2)
	lm.reset()
	rm.reset()

def turn_right (duration):
	#sl = int(speed_left)
	#sr = int(speed_right)
	t = turn_convert(int(duration))
	lm.reset()
	rm.reset()
	lm.reset()
	rm.reset()
	lm.run_to_rel_pos(position_sp = t, speed_sp = 120, stop_action = "brake")
	rm.run_to_rel_pos(position_sp = -t, speed_sp = -120, stop_action = "brake")
	lm.wait_while('running')
	rm.wait_while('running')
	time.sleep(1)
	lm.reset()
	rm.reset()

def turn_left (duration):
	#sl = int(speed_left) 
	#sr = int(speed_right) 
	t = turn_convert(int(duration))
	lm.reset()
	rm.reset()
	lm.reset()
	rm.reset()
	lm.run_to_rel_pos(position_sp = -t, speed_sp = -120, stop_action = "brake") 
	rm.run_to_rel_pos(position_sp = t, speed_sp = 120, stop_action = "brake") 
	lm.wait_while('running') 
	rm.wait_while('running') 
	time.sleep(1) 
	lm.reset()
	rm.reset()


def turn_convert (degree):
	ans = float((degree*268)/90)
	return ans 

def dist_convert(dist):
	
	if  int(dist) == 1:
		ans = 0.05
	else:
		ans = float(int(dist)*0.05)		
	return ans 

def execute (commands_list):
	for i in range(0,len(commands_list)):
		command = commands_list[i]
		print(command)
		print(commands_list)	
		if (command[0] == "f"):
			tmp1 = command[2:-1]
			tmp2 = tmp1.split(",")
			forward (tmp2[0])
		elif (command[0] == "r"):
			tmp1 = command[2:-1]
			tmp2 = tmp1.split(",")
			turn_right (tmp2[0])
		elif (command[0] == "l"):
			tmp1 = command[2:-1]
			tmp2 = tmp1.split(",")
			turn_left (tmp2[0])
		elif (command[0] == "x"):
			strval = ""
			for k in range(1, len(command)):
				strval += command[k]
			repeat = int(strval)
			repeat_execute(commands_list[:i], repeat) 	
		else:
			print("Not a valid command")


def repeat_execute(commands_list, iter_num):
	for i in range(0, iter_num-1 ):
		execute(commands_list)


if __name__ == "__main__":
	commands = argv[1]
	commands_list = commands.split(" ")
	execute(commands_list)
