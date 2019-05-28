import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from map_nodes import Node 
from map_edges import Edge
from graph_functions import plot_graph
from process_data import process_data
# from neighborhood_dijkstra import NeighborhoodDijkstra
from Dijkstra_npq import Dijkstra
from priority_queue import NaivePriorityQueue
from neighborhood import Neighborhood
from neighborhood_functions import find_neighbors
from data_functions import save_to_file, load_from_file
print('start')

#=====================================================================================================
#=====================================================================================================

def hexagon(center,size):
	x_vals = []
	y_vals = []
	for i in range(7):
		deg = (60*i)-30
		rad = deg*np.pi/180

		x_vals.append(center[0]+size*np.cos(rad))
		y_vals.append(center[1]+size*np.sin(rad))

	return x_vals,y_vals

#=====================================================================================================

def tile_hex(zero,rows,cols,ax,size,color,nodes,draw=False):
	hexes = []
	centers = []
	corners = []
	for i in range(rows):
		for j in range(cols):
			if i%2 == 0:
				center = [zero[0]+(j*np.sqrt(3)*size)+(np.sqrt(3)*size)/2,zero[1]+i*(2*size*0.75)]
			else:
				center = [zero[0]+(j*np.sqrt(3)*size)+(np.sqrt(3)*size)/2+(i-(i-1))*(np.sqrt(3)*size)/2,zero[1]+i*(2*size*0.75)]
			x,y = hexagon(center,size)
			# if i == 5 and j == 5:
				# h = gather_hex_points(x,y,nodes)
				# exits = find_exits(h,[x,y],center,size)
				# for p in h:
				# 	ax.scatter(p.x,p.y,s=50,c='r')
				# for n in exits:
				# 	ax.scatter(n.x,n.y,s=50,c='b')
				# print(exits)
				# color = 'b'
			hexes.append(gather_hex_points(x,y,nodes))
			centers.append(center)
			corners.append([x,y])
			# color = 'b'
			if draw:
				ax.plot(x,y,color)
			# color = 'r'
	return hexes,centers,corners

#=====================================================================================================

def gather_hex_points(x,y,nodes):
	m1,b1 = slope_intercept((x[0],y[0]),(x[1],y[1]))
	m2,b2 = slope_intercept((x[1],y[1]),(x[2],y[2]))
	m3,b3 = slope_intercept((x[2],y[2]),(x[3],y[3]))
	m4,b4 = slope_intercept((x[3],y[3]),(x[4],y[4]))
	m5,b5 = slope_intercept((x[4],y[4]),(x[5],y[5]))
	m6,b6 = slope_intercept((x[5],y[5]),(x[6],y[6]))

	points = []

	for key in nodes:
		col,row = nodes[key].x,nodes[key].y
		cond1 = col <= b1
		cond2 = row <= m2*col+b2
		cond3 = row <= m3*col+b3
		cond4 = col >= b4
		cond5 = row >= m5*col+b5
		cond6 = row >= m6*col+b6

		if cond1 and cond2 and cond3 and cond4 and cond5 and cond6:
			points.append(nodes[key])

	return points

#=====================================================================================================

def slope_intercept(p1,p2):
	'''Equation for a line derived from two points'''
	# slope = 1.0*(p2[0]-p1[0])/(p2[1]-p1[1])
	# intercept = p2[0]-slope*p2[1]

	if (p2[0]-p1[0]) != 0:
		slope = (p2[1]-p1[1])/(p2[0]-p1[0])
		intercept = p1[1]-slope*p1[0]
	else:
		slope = 0
		intercept = p1[0]

	return slope,intercept

#=====================================================================================================

def line_equ(pt1 , pt2):
	# finds the equation of the line connecting two points in the form ay+bx+c=0
	x1,y1 = pt1
	x2,y2 = pt2
	# print(x1,y1)
	# print(x2,y2)
	# print("-------------------------------------C")
	a = y2 - y1
	b = x2 - x1
	c = a*(-1*x1) - b*(-1*y1) 
	return (a,-b,c)

#=====================================================================================================

def line_dist(line_equ,pt1):
	# finds the perpedicular distance from a line to a point
	x,y = pt1
	a,b,c = line_equ
	d = np.abs(a*x+b*y+c)/np.sqrt(a**2 + b**2)
	return d

#=====================================================================================================

def find_exits(nodes,corners,center,size):
	if len(nodes) == 0:
		return None,None

	# xc,yc = center
	# initilize nonlinear portions of the equations
	# right = size*np.sin(2*np.pi/3)
	# up = size*np.cos(2*np.pi/3)
	# # calculate the six corners
	# pt1 = (xc,yc+size)
	# pt2 =  (xc+right,yc+up)
	# pt3 = (xc+right,yc-up)
	# pt4 = (xc,yc-size)
	# pt5 = (xc-right,yc-up)
	# pt6 = (xc-right,yc+up)
	pts = []
	# print(corners)
	x,y = corners 
	for i in range(len(x)):
		pts.append([x[i],y[i]])
	# finds equations of the lines connecting the points
	lines = []
	for i in range(len(pts)-1):
		lines.append(line_equ(pts[i],pts[i+1]))
	# print(lines)
	# lines = [line_equ(pt1,pt2),line_equ(pt2,pt3),line_equ(pt3,pt4),line_equ(pt4,pt5),line_equ(pt5,pt6),line_equ(pt6,pt1)]
	#calculates the distances between each point and line
	distances = np.zeros((6,len(nodes)))
	indexes = []
	for i in range(len(nodes)):
		for j in range(6):
			x = nodes[i].x
			y = nodes[i].y
			distances[j,i] = line_dist(lines[j],(x,y))
		indexes.append(i)

	# finds the minimum distance for each line
	# print(distances.keys())
	# print(distances)
	exit = []
	final_dist = []
	for i in range(6):
		min_dist = np.min(distances[i,:])
		min_index = np.where(distances[i,:]==min_dist)
		# print(distances[i,:],min_node,min_index[0][0])
		exit.append(nodes[min_index[0][0]])
		final_dist.append(min_dist)
		# min_node = np.min()
		# exit.append(nodes[])

	# print(final_dist)
	
	return exit,final_dist

#=====================================================================================================

def process_neighborhoods(west,south,rows,columns,ax,size,nodes,draw=False):
	hexes,centers,corners = tile_hex((west-0.006,south+0.002),rows,columns,ax,size,'b',nodes,draw=draw)

	print(len(nodes),len(hexes))

	# print(hex_dict.keys())

	neighborhoods = []
	for i in range(len(hexes)):
		current_center = centers[i]
		current_corners = corners[i]

		exits, distances= find_exits(hexes[i],current_corners,current_center,size)
		# print(exits)
		# print(len(hexes[i]),len(exits))

		nh = Neighborhood()
		nh.setNodes(hexes[i])
		nh.setCorners(current_corners)
		nh.setCenter(current_center)
		nh.setExits(exits)
		nh.setDistances(distances)

		if exits == None:
			nh = None

		neighborhoods.append(nh)

		if exits == None:
			continue

		# if draw:
		# 	for n in exits:
		# 		ax.scatter(n.x,n.y,s=50,c='b')

	hex_dict = find_neighbors(neighborhoods,columns)
	for i in range(len(neighborhoods)):
		if neighborhoods[i] != None:
			neighborhoods[i].setNeighbors(hex_dict[i])
			neighborhoods[i].setID(i)

	return neighborhoods

#=====================================================================================================

def fix_entrances(neighborhoods,ax):
	for nh in neighborhoods:
		if nh == None:
			continue
		exits = nh.getExits()
		distances = nh.getDistances()
		neighbors = nh.getNeighbors()

		# print(distances,exits)

		for i in range(len(exits)):
			if neighbors[i] != None:
				if neighborhoods[neighbors[i]] != None: 
					entrance = neighborhoods[neighbors[i]].getDistances()[i-3]
					n_exit = neighborhoods[neighbors[i]].getExits()[i-3]
					# ax.plot((n_exit.x,exits[i].x),(n_exit.y,exits[i].y),'#39ff14',zorder=10)
					if distances[i] > entrance:
						exits[i] = n_exit
		nh.setExits(exits)

	return neighborhoods

#=====================================================================================================

def find_internal_paths(neighborhoods,nodes,edges,ax):
	loop_count = 0
	for nh in neighborhoods:
		if nh == None:
			continue
		neighbors = nh.getNeighbors()
		print('Neighborhood ',loop_count)
		exits = nh.getExits()
		paths = {}
		for i in range(len(exits)):
			start = exits[i].getID()
			for j in range(i,len(exits)):
				end = exits[j].getID()
				d = Dijkstra(nodes,edges,ax)
				path,cost = d.search(start,end,'r')
				if exits[i].getID() in paths:
					paths[exits[i].getID()].append([cost,path,neighbors[j]])
				else:
					paths[exits[i].getID()] = [[cost,path,neighbors[j]]]

				if exits[j].getID() in paths:
					paths[exits[j].getID()].append([cost,path,neighbors[i]])
				else:
					paths[exits[j].getID()] = [[cost,path,neighbors[i]]]

		nh.setPaths(paths)
		loop_count += 1
		print('===============')
	return neighborhoods

#=====================================================================================================
#=====================================================================================================

G = ox.save_load.load_graphml('graph.graphml')

print('We have the graph')

nodes,edges = process_data(G)
g_edges = ox.graph_to_gdfs(G, nodes=False, fill_edge_geometry=True)
west, south, east, north = g_edges.total_bounds

# f = open("bounds.txt", "a")
# st = str(north)+","+str(east)+","+str(south)+","+str(west)
# print(st)
# f.write(st)
# f.write("\n")

# print(north,east,south,west)
fig,ax = plot_graph(nodes,edges,north,west,east,south,color_types=False,show=False)

# _nh,_n,_e = load_from_file('test')
# fig1,ax1 = plot_graph(_n,_e,north,west,east,south,color_types=False,show=False)

size = 0.005
w = np.sqrt(3)*size
width = abs(west)-abs(east)
height = abs(north)-abs(south)
rows = int(height/w+3)
columns = int(width/w+1)
# print(rows,columns)

neighborhoods = process_neighborhoods(west,south,rows,columns,ax,size,nodes,draw=True)
neighborhoods = fix_entrances(neighborhoods,ax)
neighborhoods = find_internal_paths(neighborhoods,nodes,edges,ax)
# print(len(neighborhoods))

# print(len(neighborhoods)-count)

save_to_file('test',neighborhoods,nodes,edges)

plt.show()
print('all done')