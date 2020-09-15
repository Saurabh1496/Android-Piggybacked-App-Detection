import os
import glob
import networkx as nx

def get_proper(input_string):
	types_mapping = {'V' : 'void', 'Z' : 'boolean', 'C' : 'char',
					'B' : 'byte', 'S' : 'short', 'I' : 'int',
					'J' : 'long', 'F' : 'float', 'D' : 'double'}

	input_list = list()
	if input_string:
		input_list = input_string.replace('/', '.').strip(';').split(';')
		
	result = list()

	for unformat_input in input_list:
		if len(unformat_input) == 0:
			result.append(unformat_input)
		elif len(unformat_input) == 1:
			if unformat_input in types_mapping:
				result.append(types_mapping[unformat_input])
			else:
				result.append(unformat_input)
		else:
			brack = 0
			for i in range(len(unformat_input)):
				if unformat_input[i] == 'L':
					result.append(unformat_input[i + 1:] + '[]' * brack)
					break
				elif unformat_input[i] == '[':
					brack += 1
				else:
					if unformat_input[i] in types_mapping:
						result.append(types_mapping[unformat_input[i]] + '[]'*brack)
					else:
						result.append(unformat_input[i] + '[]'*brack)
					break
	return result

def get_proper_caller(caller_sign):
	caller_method, remaining = caller_sign.split('(')
	caller_args, caller_ret = remaining.split(')')
	return caller_method, ','.join(get_proper(caller_args)), get_proper(caller_ret)[0]
	
def get_proper_callee(callee_sign):
	sign_list = callee_sign.split(';->')
	if (len(sign_list) == 2):
		callee_class, remaining = sign_list
		callee_method, callee_args, callee_ret = get_proper_caller(remaining)
		return callee_class[1:].replace('/', '.'), callee_method, callee_args, callee_ret

def save_call(file, graph):
	caller_class = ''
	for line in file:
		if not caller_class:
			caller_class = line.split()[-1][1:-1].replace('/', '.')
		if (line[:7] == '.method'):
			caller_sign = line.split()[-1]
			caller_method, caller_args, caller_return = get_proper_caller(caller_sign)
		elif 'invoke-' in line:
			callee_sign = line.split()[-1]
			formatted_callee = get_proper_callee(callee_sign)
			if formatted_callee:
				callee_class, callee_method, callee_args, callee_return = formatted_callee
				caller = '<{}: {} {}({})>'.format(caller_class,caller_return,caller_method,caller_args)
				callee = '<{}: {} {}({})>'.format(callee_class,callee_return,callee_method,callee_args)
				if not graph.has_node(caller):
					graph.add_node(caller)
				if not graph.has_node(callee):
					graph.add_node(callee)
				graph.add_edge(caller, callee)

def gen_call_graph(disassemble_loc):
	smali_files = list()

	folders_name_list = list(filter(lambda name: name.startswith('smali'), os.listdir(disassemble_loc)))
	folders_path = [disassemble_loc + folder for folder in folders_name_list]
	for folder_location in folders_path:
		smali_files.extend(glob.glob(folder_location + '/**/*.smali', recursive=True))

	graph = nx.DiGraph()
	for smali in smali_files:
		with open(smali) as file:
			save_call(file, graph)
			
	return graph