import pickle

def convert_to_binary_feature(permission_list):
	with open('permission_to_index', 'rb') as f:
		permission_dict = pickle.load(f)

	binary_list = [0] * len(permission_dict)

	for perm in permission_list:
		if perm in permission_dict:
			binary_list[permission_dict[perm]] = 1
	return binary_list

def extract_perm_features(disassemble_loc):
	manifest_file = disassemble_loc + 'AndroidManifest.xml'
	permission_list = list()

	with open(manifest_file) as file:
		for line in file:
			line = line.strip()
			if line.startswith('<uses-permission'):
				perm_start_index = line.find('.permission.')
				if perm_start_index != -1:
					end_index = line.find('"', perm_start_index)
					permission_list.append(line[perm_start_index + 12: end_index].lower())

	return convert_to_binary_feature(permission_list)