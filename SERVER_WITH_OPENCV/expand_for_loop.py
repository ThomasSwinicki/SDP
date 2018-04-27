def find_end_paren(c_list):
	instr_list = list(map((lambda i: i[0]), c_list))
	count = 0

	for i in range(len(instr_list)):
		instr = instr_list[i]
		if instr == '(':
			count += 1
		elif instr == ')' and count == 0:
			return i
		elif instr == ')':
			count -= 1

def expand_for_loops(commands_list) -> list:
	result = []
	# i = instruction
	# p = parameter
	for i, p in commands_list:
		if i == '(':
			start  = commands_list.index((i, p)) + 1
			end    = find_end_paren(commands_list[start:]) + start 
			front  = result
			middle = expand_for_loops(commands_list[start:end]) * p
			back   = expand_for_loops(commands_list[end+1:])
			return front + middle + back
		else:
			result.append(tuple((i,p)))
		
	return result
	
def parse_commands(commands):
	to_int        = lambda s: int(s) if s.isdigit() else s
	to_tuple      = lambda t: tuple(map(to_int, t.split(',')))
	commands_list = list(map(to_tuple, commands.split(' ')))
	
	return commands_list

def rm_adjacents(robot_input):
	def add(cmd1, cmd2):
		signed  = lambda tup: -(tup[1]) if tup[0] == 'l' else tup[1]
		added   = signed(cmd1) + signed(cmd2)
		if added < 0:
			return ('l', abs(added))
		elif cmd1[0] != 'f':
			return ('r', added)
		else:
			return ('f', added)

	clean_input         = []
	is_turn             = lambda instr: True if instr == 'r' or instr == 'l' else False	
	is_forward          = lambda instr: True if instr == 'f' else False
	check_both          = lambda i1,i2: True if (is_turn(i1) and is_turn(i2)) or (is_forward(i1) and is_forward(i2)) else False
	prev_cmd,prev_num   = robot_input[0]
	input_iterator      = iter(robot_input[1:])

	for cmd,num in input_iterator:

		if check_both(prev_cmd,cmd):
			clean_input       += [add((prev_cmd,prev_num), (cmd,num))]
			try:
				prev_cmd,prev_num  = next(input_iterator)
			except:
				pass
		else:
			clean_input       += [(prev_cmd,prev_num)]
			prev_cmd,prev_num  = cmd,num
	
	cmd,num           = robot_input[-1]
	prev_cmd,prev_num = clean_input[-1]

	if not check_both(prev_cmd, cmd):
		clean_input += [(cmd,num)]

	return clean_input

def run_commands(commands):
	commands_list  = parse_commands(commands)
	raw_commands   = expand_for_loops(commands_list)
	final_commands = rm_adjacents(raw_commands)
	
	return final_commands
			
if __name__ == '__main__':
	commands      = argv[1]
	commands_list = parse_commands(commands)
	robot_input   = expand_for_loops(commands_list)
	print(robot_input)
	#execute(robot_input)	
