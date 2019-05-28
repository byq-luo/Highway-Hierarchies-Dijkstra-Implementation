import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from map_nodes import Node 
from map_edges import Edge
from graph_functions import plot_graph
from process_data import process_data
import Dijkstra_npq, Dijkstra_HH, Dijkstra_Neighborhood
from priority_queue import NaivePriorityQueue
from neighborhood import Neighborhood
from neighborhood_functions import find_neighbors
from data_functions import save_to_file, load_from_file
import time,random

b = open("bounds.txt",'r')

#============================================================
#============================================================

def read_line(file):
	contents = file.readline()
	output = contents.split(',')

	north = float(output[0])
	east = float(output[1])
	south = float(output[2])
	west = float(output[3])

	return north,east,south,west

#============================================================

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

#============================================================

def hex_check(col,row,corners):
	x,y = corners
	m1,b1 = slope_intercept((x[0],y[0]),(x[1],y[1]))
	m2,b2 = slope_intercept((x[1],y[1]),(x[2],y[2]))
	m3,b3 = slope_intercept((x[2],y[2]),(x[3],y[3]))
	m4,b4 = slope_intercept((x[3],y[3]),(x[4],y[4]))
	m5,b5 = slope_intercept((x[4],y[4]),(x[5],y[5]))
	m6,b6 = slope_intercept((x[5],y[5]),(x[6],y[6]))

	cond1 = col <= b1
	cond2 = row <= m2*col+b2
	cond3 = row <= m3*col+b3
	cond4 = col >= b4
	cond5 = row >= m5*col+b5
	cond6 = row >= m6*col+b6

	if cond1 and cond2 and cond3 and cond4 and cond5 and cond6:
		return True
	else:
		return False

#============================================================
#============================================================

neighborhoods,nodes,edges = load_from_file('test')

north,east,south,west = read_line(b)

fig,ax = plot_graph(nodes,edges,north,west,east,south,color_types=False,show=False)

# goal = 49171567
# start = 50651343 #50422455

#test 2
#start = 49811183
#goal = 50656963
#d time = 4.237915277481079
#hh time = 0.17772912979125977

#test 3
#start = 50445628
#goal = 50543902
#d time = 2.599471092224121
#hh time = 0.09031391143798828

#test 4
#start = 50527139
#goal = 49766358
#d time = 3.3068621158599854
#hh time = 0.09735250473022461

#test 5
#start = 49163552
#goal = 50297490
#d time = 4.064844131469727
#hh time = 0.1315751075744629

#test 6
#start = 1563065123
#goal = 50515020
#d time = 0.7622644901275635
#hh time = 0.0704648494720459

#test 7
#start = 49819801
#goal = 50229553
#d time = 3.3400192260742188
#hh time = 0.13426446914672852

#test 8
#start = 49806714
#goal = 50556577
#d time = 5.01009464263916
#hh time = 0.1676790714263916

#test 9
#start = 50315348
#goal = 50514418
#d time = 4.368917942047119
#hh time = 0.07729554176330566

#test 10
#start = 50742515
#goal = 50493250
#d time = 0.7306787967681885
#hh time = 0.0653526782989502

# print(nodes.keys())

start = random.choice(list(nodes.keys()))
goal = random.choice(list(nodes.keys()))

start_time = time.time()

d = Dijkstra_npq.Dijkstra(nodes,edges,ax)
path,cost = d.search(start,goal,'r')

print('Dijkstra Time Elapsed: ',time.time()-start_time)
print(start,goal)

start_time = time.time()

sx,sy = nodes[start].x,nodes[start].y
gx,gy = nodes[goal].x,nodes[goal].y
start_nh = -1
goal_nh = -1
start_exits = None
goal_exits = None
for i in range(len(neighborhoods)):
	nh = neighborhoods[i]
	if nh == None:
		continue
	if hex_check(sx,sy,nh.getCorners()):
		print('Start Neighborhood ',i)
		start_nh = i
		start_exits = nh.getExits()

	if hex_check(gx,gy,nh.getCorners()):
		print('Goal Neighborhood ',i)
		goal_nh = i
		goal_exits = nh.getExits()

hh = Dijkstra_HH.Dijkstra(nodes,edges,ax)
path,cost,start_exit = hh.search(start,goal,start_exits,goal_exits,search='start')

start_neighborhood = neighborhoods[start_nh]
goal_neighborhood = neighborhoods[goal_nh]

nd = Dijkstra_Neighborhood.Dijkstra(neighborhoods,nodes,edges,ax)
entrance_id = nd.search(start_neighborhood,goal_neighborhood,start_exit)

hh = Dijkstra_npq.Dijkstra(nodes,edges,ax)
hh.search(entrance_id,goal,'b')

print('HH Time Elapsed: ',time.time()-start_time)

plt.show()