import networkx as nx
from sensitive_subgraph_generator import get_api_info, subgraph_sensitivity

def total_sensitive_distance(subgraph, common_api_list):
	subgraph = nx.Graph(subgraph)
	tsd = 0.0

	num_sen_api = len(common_api_list)
	for i in range(num_sen_api):
		dist = 0.0
		sd = 0.0
		for j in range(num_sen_api):
			if i != j:
				try:
					dist += (1.0 / nx.shortest_path_length(subgraph,source=common_api_list[i],target=common_api_list[j]))
				except:
					dist += 0.0
		try:
			sd = (1 / (num_sen_api - 1)) * dist
		except:
			sd = 0.0
		tsd += sd
	return tsd

def extract_subgraph_features(subgraph):
	api_list, api_coeff = get_api_info()
	common_api = list(set(api_list).intersection(set(subgraph.nodes())))

	feature_list = []
	feature_list.append(subgraph_sensitivity(subgraph, common_api, api_coeff))
	feature_list.append(total_sensitive_distance(subgraph, common_api))
	return feature_list