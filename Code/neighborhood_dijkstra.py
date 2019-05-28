'''
@Author: Rene Jacques
March 21, 2019
'''

from node import Map_Node
from priority_queue import NaivePriorityQueue
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import math

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

class NeighborhoodDijkstra:
	'''Dijkstra Search Algorithm'''
	def __init__(self,nodes,edges,plot):
		self.nodes = nodes
		self.edges = edges
		self.ax = plot

		self.open_set = NaivePriorityQueue() 
		self.closed_set = set()
		self.h_count = 0

	#=========================================================================

	def search(self,start,H=100,closed_set=set(),display_rate=None,node_color='b'):
		'''Search for goal coordinates given start coordinates'''
		# color in start square
		sx,sy = self.nodes[start].x,self.nodes[start].y
		self.ax.scatter(sx,sy,s=50,c='k',zorder=10)
		self.closed_set = closed_set
		# color in goal square

		# gx,gy = self.nodes[goal].x,self.nodes[goal].y
		# self.ax.scatter(gx,gy,s=50,c='g',zorder=10)

		# plt.show()

		# create start node
		s = Map_Node()
		s.setID(start)

		# create goal node
		# g = Map_Node()
		# g.setID(goal)

		# add start node to open_set
		self.open_set.add(s)

		# initialize variable to check if the size of the open_set stays 1 for 5 loops
		open_count = 0

		loop_count = 0
		# search until the open_set is empty or a break is encountered
		while self.h_count < H:

			# get the next node out of the open set
			next_node = self.open_set.pop()

			# get the next nodes neighbors
			neighbors = self.get_neighbors(next_node)

			for neighbor in neighbors:
				# check if the neighbor is at the goal
				# if neighbor.getID()==goal:
				# 	print('Goal Found At:'+str(neighbor.getID()))

				# 	# show the path from goal to start
				# 	self.build_path(neighbor)
				# 	plt.pause(0.001)

				# 	plt.show()
				# 	return
				# else:
				# initialize a flag to indicate duplicates in the open and closed sets
				duplicate_flag = False

				# check if the neighbor is in the open set or the closed set
				for item in self.open_set.getQueue():
					# check if the neighbor is in the closed set
					if str(neighbor.getID()) in self.closed_set:
						duplicate_flag = True
						break

					if not duplicate_flag:
						# check if the neighbor is in the open set
						if item.getID() == neighbor.getID():
							# if the neighbor's g cost is less than a node's g cost 
							# if neighbor.getCost() < item.getCost():
							# 	self.open_set.remove(item) # remove the node from the open set
							# 	self.open_set.add(neighbor) # add the neighbor to the open set
							duplicate_flag = True
							break

				# if the neighbor is not in the open set and not in the closed set
				if not duplicate_flag:
					# add neighbor to the open set
					self.open_set.add(neighbor)
					self.h_count += 1

					try:
						graph_edge(self.edges[neighbor.getEdgeID()],self.nodes,self.ax,node_color)
						ox,oy = self.nodes[neighbor.getID()].x,self.nodes[neighbor.getID()].y
						self.ax.scatter(ox,oy,s=10,c=node_color,zorder=9)
					except:
						# print('open fail')
						pass

						
						# plt.pause(0.001)
			# add the current node to the closed set
			closed = str(next_node.getID())
			self.closed_set.add(closed)

			try:
				graph_edge(self.edges[next_node.getEdgeID()],self.nodes,self.ax,node_color)
				cx,cy = self.nodes[next_node.getID()].x,self.nodes[next_node.getID()].y
				self.ax.scatter(cx,cy,s=10,c=node_color,zorder=10)
			except:
				# print('closed fail')
				pass

			if display_rate != None:
				if loop_count%display_rate == 0:
					print(loop_count)
					plt.pause(0.0001)
					# plt.show()
			
			# plt.pause(0.001)
			
			loop_count += 1

			# if len(self.closed_set) == 100:
			# 	print('length of closed_set = 100')
			# 	plt.show()

		# if the open set is empty then there is no path possible
		return self.open_set,self.closed_set

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

	# def build_path(self,n):
	# 	'''Recursive function to build the path by searching through the parents of each node from start to goal'''
	# 	try:
	# 		graph_edge(self.edges[n.getEdgeID()],self.nodes,self.ax,'r',edge_width=3)
	# 		x,y = self.nodes[n.getID()].x,self.nodes[n.getID()].y
	# 		# self.ax.scatter(x,y,s=15,c='g',zorder=10)
	# 	except:
	# 		print('path fail')

		

	# 	# check if the next parent exists (if it does not then the end of the path has been reached)
	# 	if n.getParent() != None:
	# 		self.build_path(n.getParent())