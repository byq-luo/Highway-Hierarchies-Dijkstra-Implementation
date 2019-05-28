'''
@Author: Rene Jacques
March 21, 2019
'''

from node import NH_Node
from priority_queue import NaivePriorityQueue
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import math
import numpy as np

# define colors
yellow = (0,255,255)
cyan = (255,255,0)
white = (255,255,255)
black = (0,0,0)
gray = (50,50,50)
blue = (255,0,0)
green = (0,255,0)
red = (0,0,255)

#=========================================================================
#=========================================================================

def graph_edge(edge,nodes,ax,edge_color,edge_width=1):
	lines = []
	if edge.geo != None:
		xs, ys = edge.geo.xy
		# print(edge.geo.xy)

		lines.append(list(zip(xs, ys)))
	else:
		u,v = edge.u,edge.v
		x1 = nodes[u].x
		y1 = nodes[u].y
		x2 = nodes[v].x
		y2 = nodes[v].y

		line = [(x1, y1), (x2, y2)]
		lines.append(line)

	lc = LineCollection(lines, colors=edge_color, linewidths=edge_width, alpha=1, zorder=8)
	ax.add_collection(lc)

#=========================================================================

class Dijkstra:
	'''Dijkstra Search Algorithm'''
	def __init__(self,nodes,map_nodes,edges,plot):
		self.nodes = nodes
		self.edges = edges
		self.map_nodes = map_nodes
		self.ax = plot

		self.open_set = NaivePriorityQueue() 
		self.closed_set = set()

	#=========================================================================

	def search(self,start,goal,exit,display_rate=None):
		'''Search for goal coordinates given start coordinates'''
		# color in start square
		# sx,sy = self.nodes[start].x,self.nodes[start].y
		# self.ax.scatter(sx,sy,s=50,c='b',zorder=10)
		# # color in goal square
		# gx,gy = self.nodes[goal].x,self.nodes[goal].y
		# self.ax.scatter(gx,gy,s=50,c='g',zorder=10)

		# start_exit_ids = []
		# for s in starts:
		# 	self.ax.scatter(s.x,s.y,s=50,c='b',zorder=10)
		# 	start_exit_ids.append(s.getID())

		# goal_exit_ids = []
		# for g in goals:
		# 	self.ax.scatter(g.x,g.y,s=50,c='g',zorder=10)
		# 	goal_exit_ids.append(g.getID())

		# if search == 'start':
		# 	exit_ids = start_exit_ids
		# else:
		# 	exit_ids = goal_exit_ids

		# plt.show()

		# create start node
		s = NH_Node()
		s.setID(start.getID())
		s.setEntrance(exit.getID())

		# create goal node
		g = NH_Node()
		g.setID(goal.getID())

		# add start node to open_set
		self.open_set.add(s)

		# initialize variable to check if the size of the open_set stays 1 for 5 loops
		open_count = 0

		loop_count = 0
		# search until the open_set is empty or a break is encountered
		while not self.open_set.isEmpty() and open_count != 5:
			if(len(self.open_set.getQueue()) == 1):
				open_count += 1
			else:
				open_count = 0

			# get the next node out of the open set
			next_node = self.open_set.pop()

			# get the next nodes neighbors
			# neighbors = self.get_neighbors(next_node)
			# print(next_node.getID())
			if self.nodes[next_node.getID()] == None:
				continue
			paths = self.nodes[next_node.getID()].getPaths()[next_node.getEntrance()]

			# print(np.shape(paths))

			for p in paths:
				# check if the neighbor is at the goal
				# cost = paths[i*3]
				# nodes_path = paths[i*3+1]
				# neighbor = paths[i*3+2]
				cost,nodes_path,neighbor = p
				if neighbor == None or nodes_path == None:
					continue

				# print(nodes_path[0])
				nn = NH_Node()
				# print(cost,next_node.getCost(),nodes_path)
				nn.setCost(cost+next_node.getCost())
				nn.setID(neighbor)
				nn.setPath(nodes_path)
				nn.setParent(next_node)

				if next_node.getEntrance() == nodes_path[0].getID():
					nn.setEntrance(nodes_path[-1].getID()) 
				else:
					nn.setEntrance(nodes_path[0].getID())

				if neighbor == goal.getID():
					print('Goal Found At:'+str(neighbor))

					# show the path from goal to start
				
					self.build_path(nn)
					# plt.pause(0.001)

					# plt.show()

					return nn.getEntrance()
				else:
					# initialize a flag to indicate duplicates in the open and closed sets
					duplicate_flag = False 

					# check if the neighbor is in the open set or the closed set
					for item in self.open_set.getQueue():
						# check if the neighbor is in the closed set
						if str(neighbor) in self.closed_set:
							duplicate_flag = True
							break

						if not duplicate_flag:
							# check if the neighbor is in the open set
							if item.getID() == neighbor:
								# if the neighbor's g cost is less than a node's g cost 
								if cost < item.getCost():
									self.open_set.remove(item) # remove the node from the open set
									self.open_set.add(nn) # add the neighbor to the open set
								duplicate_flag = True
								break

					# if the neighbor is not in the open set and not in the closed set
					if not duplicate_flag:
						# add neighbor to the open set
						self.open_set.add(nn)

						# try:
						# 	graph_edge(self.edges[neighbor.getEdgeID()],self.nodes,self.ax,'b')
						# 	ox,oy = self.nodes[neighbor.getID()].x,self.nodes[neighbor.getID()].y
						# 	self.ax.scatter(ox,oy,s=10,c='b',zorder=9)
						# except:
						# 	print('open fail')

						
						# plt.pause(0.001)
			# add the current node to the closed set
			closed = str(next_node.getID())
			self.closed_set.add(closed)

			# try:
			# 	graph_edge(self.edges[next_node.getEdgeID()],self.nodes,self.ax,'y')
			# 	cx,cy = self.nodes[next_node.getID()].x,self.nodes[next_node.getID()].y
			# 	self.ax.scatter(cx,cy,s=10,c='y',zorder=10)
			# except:
			# 	print('closed fail')

			if display_rate != None:
				if loop_count%display_rate == 0:
					print(loop_count)
					plt.pause(0.0001)
			
			# plt.pause(0.001)
			
			loop_count += 1

			# if len(self.closed_set) == 100:
			# 	print('length of closed_set = 100')
			# 	plt.show()

		# if the open set is empty then there is no path possible
		if self.open_set.isEmpty() or open_count ==5:
			print('No Path Possible')
		# cv2.waitKey(0)
		return None,None

	#=========================================================================

	def get_neighbors(self,n):
		'''Get all of the neighbors for the input node'''
		neighbors = []
		options = self.nodes[n.getID()].edges

		# get each neigbor to the top left, top middle, top right, right middle, bottom right, bottom middle, bottom left, left middle
		for e in options:
			neighbor = Map_Node()

			if self.edges[e].u != n.getID():
				neighbor.setID(self.edges[e].u)
			elif self.edges[e].v != n.getID():
				neighbor.setID(self.edges[e].v)
			else:
				continue

			# print(neighbor.getID())

			neighbor.setParent(n)
			neighbor.setEdgeID(e)
			neighbor.setCost(n.getCost()+(self.edges[e].length/self.edges[e].weight))
			neighbors.append(neighbor)

		return neighbors

	#=========================================================================

	def build_path(self,n):
		'''Recursive function to build the path by searching through the parents of each node from start to goal'''
		# try:
		# 	graph_edge(self.edges[n.getEdgeID()],self.nodes,self.ax,'c',edge_width=3)
		# 	x,y = self.nodes[n.getID()].x,self.nodes[n.getID()].y
		# 	# self.ax.scatter(x,y,s=15,c='g',zorder=10)
		# except:
		# 	# print('path fail')
		# 	pass
		path = n.getPath()
		if path != None:
			for p in path:
				# print(p.getID())
				try:
					graph_edge(self.edges[p.getEdgeID()],self.map_nodes,self.ax,'b',edge_width=3)
					# x,y = self.map_nodes[p.getID()].x,self.map_nodes[p.getID()].y
					# self.ax.scatter(x,y,s=15,c='b',zorder=10)
				except:
					pass

		# check if the next parent exists (if it does not then the end of the path has been reached)
		if n.getParent() != None:
			self.build_path(n.getParent())