class Neighborhood:
	def __init__(self):
		self.nodes = None
		self.corners = None
		self.center = None
		self.exits = None
		self.distances = None
		self.id = None

		self.paths = None

		self.neighbors = [0,0,0,0,0,0] #east, north east, north west, west, south west, south east

	def setNodes(self,nodes):
		self.nodes = nodes 

	def getNodes(self):
		return self.nodes

	def setCorners(self,corners):
		self.corners = corners

	def getCorners(self):
		return self.corners

	def setCenter(self,center):
		self.center = center

	def getCenter(self):
		return self.center

	def setExits(self,exits):
		self.exits = exits

	def getExits(self):
		return self.exits

	def addNeighbor(self,neighbor,index):
		self.neighbors[index] = neighbor

	def getNeighbors(self):
		return self.neighbors

	def setNeighbors(self,neighbors):
		self.neighbors = neighbors

	def setDistances(self,distances):
		self.distances = distances

	def getDistances(self):
		return self.distances

	def setPaths(self,paths):
		self.paths = paths

	def getPaths(self):
		return self.paths

	def setID(self,ID):
		self.id = ID

	def getID(self):
		return self.id