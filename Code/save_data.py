import pickle

def save_object_list(filename,obj_list):
	with open(filename,'wb') as output:
		pickle.dump(obj_list,output,pickle.HIGHEST_PROTOCOL)

def save_to_file(file,neighborhoods,nodes,edges):
	save_object_list(file+'_neighborhoods.pkl',neighborhoods)
	save_object_list(file+'_nodes.pkl',nodes)
	save_object_list(file+'_edges.pkl',edges)