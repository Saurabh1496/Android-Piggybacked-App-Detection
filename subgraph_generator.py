import networkx as nx

def find_neighbors(G, api):
	first = list(G.neighbors(api))
	second = []
	for node in first:
		second = list(set(second) | set(G.neighbors(node)))
	result = list(set(first) | set(second))
	if api not in result:
		result.append(api)
	return result

def make_graph(call_graph, adj):
	subgraph = nx.DiGraph()
	if len(adj) == 1:
		subgraph.add_node(adj[0])
		return subgraph
	for i in range(len(adj)):
		for j in range(i + 1, len(adj)):
			if not subgraph.has_node(adj[i]):
				subgraph.add_node(adj[i])
			if not subgraph.has_node(adj[j]):
				subgraph.add_node(adj[j])
			if call_graph.has_edge(adj[i], adj[j]):
				subgraph.add_edge(adj[i], adj[j])
			elif call_graph.has_edge(adj[j], adj[i]):
				subgraph.add_edge(adj[j], adj[i])
	return subgraph

def check_added(subgraph_list, subgraph):
	for graph in subgraph_list:
		if graph.nodes() == subgraph.nodes() and graph.edges() == subgraph.edges():
			return True
	return False

def gen_subgraph_list(call_graph, common_api):
	G = nx.Graph(call_graph)
	subgraph_list = []

	for api in common_api:
		adj = find_neighbors(G, api)

		subgraph = make_graph(call_graph, adj)
		if not check_added(subgraph_list, subgraph):
			subgraph_list.append(subgraph)
	return subgraph_list