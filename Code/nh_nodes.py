class Node:
	def __init__(self):
		self.x = None
		self.y = None
		self.edges = []

		self.id = None

		self.entrance = None

	def setCoords(self,point):
		self.x = point.x
		self.y = point.y

	def addEdge(self,edge):
		self.edges.append(edge)

	def setID(self,ID):
		self.id = ID

	def getID(self):
		return self.id

	def setEntrance(self,entrance):
		self.entrance = entrance

	def getEntrance(self):
		return self.entrance