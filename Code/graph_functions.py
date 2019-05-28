import osmnx as ox
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt

def plot_graph(nodes,edges,north,west,east,south,
				equal_aspect=False, color_types=False, show=False, margin=0.02,
			   save=False, node_color='#66ccff', node_size=15,
			   node_alpha=1, node_edgecolor='none', node_zorder=1,
			   edge_color='#999999', edge_linewidth=1, edge_alpha=1,
			   use_geom=True):

	print('plotting')
	node_Xs = [nodes[key].x for key in nodes]
	node_Ys = [nodes[key].y for key in nodes]

	# edges = ox.graph_to_gdfs(G, nodes=False, fill_edge_geometry=True)
	# west, south, east, north = edges.total_bounds

	# if caller did not pass in a fig_width, calculate it proportionately from
	# the fig_height and bounding box aspect ratio
	bbox_aspect_ratio = (north-south)/(east-west)
	fig_height = 6
	fig_width = fig_height / bbox_aspect_ratio

	# create the figure and axis
	bgcolor = 'w'
	fig, ax = plt.subplots(figsize=(fig_width, fig_height), facecolor=bgcolor)
	ax.set_facecolor(bgcolor)

	# draw the edges as lines from node to node
	lines = []
	if color_types:
		edge_color = []
	# print(len(edges))
	for key in edges:
		# print(e)
		if edges[key].geo != None:
			# if it has a geometry attribute (a list of line segments), add them
			# to the list of lines to plot
			xs, ys = edges[key].geo.xy
			# print(xs,ys)
			lines.append(list(zip(xs, ys)))
		# 	# if it doesn't have a geometry attribute, the edge is a straight
		# 	# line from node to node
		else:
			u,v = edges[key].u,edges[key].v
			x1 = nodes[u].x
			y1 = nodes[u].y
			x2 = nodes[v].x
			y2 = nodes[v].y
			# print(x1,y1,x2,y2)
			line = [(x1, y1), (x2, y2)]
			lines.append(line)

		if color_types:
			if edges[key].type == 'highway':
				edge_color.append('b')
			elif edges[key].type == 'primary':
				edge_color.append('r')
			elif edges[key].type == 'secondary':
				edge_color.append('c')
			elif edges[key].type == 'residential':
				edge_color.append('y')
			elif edges[key].type == 'unknown':
				edge_color.append('k')

	# add the lines to the axis as a linecollection
	lc = LineCollection(lines, colors=edge_color, linewidths=edge_linewidth, alpha=edge_alpha, zorder=2)
	ax.add_collection(lc)

	# scatter plot the nodes
	ax.scatter(node_Xs, node_Ys, s=node_size, c=node_color, alpha=node_alpha, edgecolor=node_edgecolor, zorder=node_zorder)

	# set the extent of the figure
	margin_ns = (north - south) * margin
	margin_ew = (east - west) * margin
	ax.set_ylim((south - margin_ns, north + margin_ns))
	ax.set_xlim((west - margin_ew, east + margin_ew))

	# configure axis appearance
	xaxis = ax.get_xaxis()
	yaxis = ax.get_yaxis()

	xaxis.get_major_formatter().set_useOffset(False)
	yaxis.get_major_formatter().set_useOffset(False)

	ax.axis('off')
	ax.margins(0)
	ax.tick_params(which='both', direction='in')
	xaxis.set_visible(False)
	yaxis.set_visible(False)
	fig.canvas.draw()

	if equal_aspect:
		# make everything square
		ax.set_aspect('equal')
		fig.canvas.draw()

	if show:
		plt.show()
	print('end plotting')
	return fig, ax