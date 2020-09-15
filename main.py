import os
import time
import sys
import shutil
import networkx as nx
from call_generator import gen_call_graph
from sensitive_subgraph_generator import gen_sensitive_subgraph
from subgraph_features import extract_subgraph_features
from permission_features import extract_perm_features
from classifier import predict

def main(path):
	start = time.time()
	os.system('apktool -f d {}'.format(path))
	disassemble_location = './{}/'.format(path[:-4])
	print('Disassembling of the APK Completed in {} seconds'.format(time.time() - start))
	
	start = time.time()
	call_graph = gen_call_graph(disassemble_location)
	print('Genration of Call Graph Completed in {} seconds'.format(time.time() - start))
	
	start = time.time()
	sensitive_subgraph = gen_sensitive_subgraph(call_graph)
	print('Genration of Sensitive Subgraph Completed in {} seconds'.format(time.time() - start))

	if sensitive_subgraph:
		subgraph_feature_list = extract_subgraph_features(sensitive_subgraph)
	else:
		subgraph_feature_list = [0.0, 0.0]

	permission_feature_list = extract_perm_features(disassemble_location)
	combined_features = subgraph_feature_list + permission_feature_list

	predict(combined_features)
	shutil.rmtree(disassemble_location)
		

if __name__ == '__main__':
	length = len(sys.argv)
	if length < 2:
		print('Please give an APK file-name as command-line argument')
		exit()
	main(sys.argv[1])