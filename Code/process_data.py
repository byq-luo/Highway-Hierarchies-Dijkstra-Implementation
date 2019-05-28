import osmnx as ox
from map_nodes import Node 
from map_edges import Edge

def process_data(G):

	graph_nodes,graph_edges = ox.graph_to_gdfs(G)

	N = {}
	E = {}

	for p,i in zip(graph_nodes['geometry'],graph_nodes['osmid']):
		n = Node()
		n.setCoords(p)
		n.setID(i)
		N[i] = n
		# print(i)

	print('------------------')

	key_count = 0
	for u,v,keys,data in G.edges(keys=True, data=True):
		# print(data.keys())
		e = Edge()
		e.setLength(data['length'])
		if data['highway'] == 'motorway' or data['highway'] == 'motorway_link' or data['highway'] == 'trunk' or data['highway'] == 'trunk_link':
			e.setType('highway')
			e.setWeight(65)
		elif data['highway'] == 'primary' or data['highway'] == 'primary_link':
			e.setType('primary')
			e.setWeight(45)
		elif data['highway'] == 'secondary' or data['highway'] == 'secondary_link' or data['highway'] == 'tertiary' or data['highway'] == 'tertiary_link':
			e.setType('secondary')
			e.setWeight(35)
		elif data['highway'] == 'residential' or data['highway'] == 'unclassified':
			e.setType('residential')
			e.setWeight(25)
		else:
			e.setType('unknown')
			e.setWeight(25)

		# if 'maxspeed' in data:
		# 	print(data['maxspeed'],data['highway'])
		# 	e.setWeight(data['maxspeed'])
		e.setID(data['osmid'])
		if 'geometry' in data:
			e.setGeometry(data['geometry'])
		e.setUV(u,v)

		if u in N:
			N[u].addEdge(key_count)
		if v in N:
			N[v].addEdge(key_count)
		# print(u,v)
		# print(data['osmid'])
		E[key_count] = e
		key_count += 1

	return N,E