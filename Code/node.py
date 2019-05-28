'''
@Author: Rene Jacques
March 17, 2019
'''

class Node:
	'''Node used as a storage object to keep track of specific data, node location in tree (ID), and node parent'''
	def __init__(self):
		self.data = None
		self.data_number = None
		self.parent = None
		self.id = None
		self.cost = None

	def setCost(self,c):
		'''Set cost to reach for this node'''
		self.cost = c 

	def getCost(self):
		'''Return cost to reach'''
		return self.cost

	def setData(self,d):
		'''Set data for this node'''
		self.data = d 

	def getData(self):
		'''Return data'''
		return self.data

	def setID(self,i):
		'''Set node ID'''
		self.id = i

	def getID(self):
		'''Return node ID'''
		return self.id

	def setParent(self,p):
		'''Set node parent'''
		self.parent = p

	def getParent(self):
		'''Return node parent'''
		return self.parent

class Map_Node(Node):
	'''Mapping Node (Extends Node)'''
	def __init__(self):
		Node.__init__(self)
		self.g = 0 # cost to come
		self.node_id = None
		self.parent_edge_id = None

		self.parent = None

	def setCost(self,g):
		'''Set g and h cost for this node'''
		self.g = g

	def getCost(self):
		'''Get g, h, and f costs for this node'''
		return self.g

	def setEdgeID(self,ID):
		self.parent_edge_id = ID

	def getEdgeID(self):
		return self.parent_edge_id

	def setID(self,ID):
		self.node_id = ID

	def getID(self):
		return self.node_id

	def setParent(self,n):
		'''Set the path parent for this node'''
		self.parent = n

	def getParent(self):
		'''Get the path parent for this node'''
		return self.parent

class NH_Node(Map_Node):
	def __init__(self):
		Map_Node.__init__(self)
		self.entrance = None
		self.path = None

	def setEntrance(self,entrance):
		self.entrance = entrance

	def getEntrance(self):
		return self.entrance

	def setPath(self,path):
		self.path = path

	def getPath(self):
		return self.path