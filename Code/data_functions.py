import pickle

def save_object_list(filename,obj_list):
	with open(filename,'wb') as _output:
		pickle.dump(obj_list,_output,pickle.HIGHEST_PROTOCOL)

def save_to_file(file,neighborhoods,nodes,edges):
	save_object_list(file+'_neighborhoods.pkl',neighborhoods)
	save_object_list(file+'_nodes.pkl',nodes)
	save_object_list(file+'_edges.pkl',edges)

def load_object_list(filename):
	with open(filename,'rb') as _input:
		obj_list = pickle.load(_input)
	return obj_list

def load_from_file(file):
	neighborhoods = load_object_list(file+'_neighborhoods.pkl')
	nodes = load_object_list(file+'_nodes.pkl')
	edges = load_object_list(file+'_edges.pkl')
	return neighborhoods,nodes,edges