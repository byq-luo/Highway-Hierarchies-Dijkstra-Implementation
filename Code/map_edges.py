class Edge:
	def __init__(self):
		self.nodes = []
		self.length = None
		self.type = None
		self.weight = None

		self.u = None
		self.v = None

		self.geo = None

		self.id = None

	def addNode(self,node):
		if len(self.nodes) < 2:
			self.nodes.append(node)
		else:
			raise Exception('This edge already has two nodes.')

	def setLength(self,length):
		self.length = length

	def setType(self,t):
		self.type = t 

	def setWeight(self,weight):
		self.weight = weight

	def setID(self,ID):
		self.id = ID

	def getID(self):
		return self.id

	def setGeometry(self,geo):
		self.geo = geo

	def setUV(self,u,v):
		self.u = u
		self.v = v