import networkx as nx
from subgraph_generator import gen_subgraph_list

def get_api_info():
	with open('Sensitive') as f:
		lines = f.readlines()
	lines = [line.strip().split('#') for line in lines]

	api_list = [line[0] for line in lines]
	api_coeff = {line[0]: float(line[1]) for line in lines}
	return api_list, api_coeff

def merge_subgraphs(subgraph_list, common_api_list):
	combining = True
	while combining:
		combining = False
		num_of_subgraphs = len(subgraph_list)
		for i in range(num_of_subgraphs):
			for j in range(i + 1, num_of_subgraphs):
				G = subgraph_list[i]
				H = subgraph_list[j]
				G_sensitive_api = list(set(common_api_list).intersection(set(G.nodes())))
				H_sensitive_api = list(set(common_api_list).intersection(set(H.nodes())))
				if set(G_sensitive_api).intersection(set(H_sensitive_api)):
					I = nx.compose(G,H)
					subgraph_list = list((set(subgraph_list) | set([I])) - set([G,H]))
					combining = True
					break
			if num_of_subgraphs != len(subgraph_list):
				break

def subgraph_sensitivity(graph, api_list, sen_coeff):
	common_api = list(set(api_list).intersection(set(graph.nodes())))
	return sum(map(lambda api: sen_coeff[api], common_api))

def gen_sensitive_subgraph(call_graph):
	api_list, api_coeff = get_api_info()
	common_api = list(set(api_list).intersection(set(call_graph.nodes())))

	subgraph_list = gen_subgraph_list(call_graph, common_api)
	merge_subgraphs(subgraph_list, common_api)

	try:
		sensitive_subgraph = max(subgraph_list, key = lambda graph: subgraph_sensitivity(graph, common_api, api_coeff))
	except:
		sensitive_subgraph = []

	return sensitive_subgraph