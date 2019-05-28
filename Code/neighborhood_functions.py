def find_neighbors(hexes,cols):
	count = 0
	rows = 0
	hex_dict = {}
	for i in range(len(hexes)):
		if count%cols == 0:
			rows += 1
		count += 1

		#-----------------------------------------------
		if i%cols == 0: #left side
			#-----------------------------------------------
			if rows %2 == 0: #even row
				#++++++++++++++++++++++++++++++
				if i+1 < len(hexes):
					E = i+1
				else:
					E = None
				#++++++++++++++++++++++++++++++
				if i+cols+1 < len(hexes):
					NE = i+cols+1
				else:
					NE = None
				#++++++++++++++++++++++++++++++
				if i+cols < len(hexes):
					NW = i+cols
				else:
					NW = None
				#++++++++++++++++++++++++++++++
				W = None
				#++++++++++++++++++++++++++++++
				if i-cols >= 0:
					SW = i-cols
				else:
					SW = None
				#++++++++++++++++++++++++++++++
				if i-cols+1 >= 0:
					SE = i-cols+1
				else:
					SE = None
				#++++++++++++++++++++++++++++++
				hex_dict[i] = [E,NE,NW,W,SW,SE]

			#-----------------------------------------------
			elif rows %2 != 0: #odd row
				#++++++++++++++++++++++++++++++
				if i+1 < len(hexes):
					E = i+1
				else:
					E = None
				#++++++++++++++++++++++++++++++
				if i+cols+1 < len(hexes):
					NE = i+cols
				else:
					NE = None
				#++++++++++++++++++++++++++++++
				# if i+cols < len(hexes):
				# 	NW = hexes[i+cols]
				# else:
				NW =None
				#++++++++++++++++++++++++++++++
				W = None
				#++++++++++++++++++++++++++++++
				# if i-cols >= 0:
				# 	SW = hexes[i-cols]
				# else:
				SW = None
				#++++++++++++++++++++++++++++++
				if i-cols+1 >= 0:
					SE = i-cols
				else:
					SE = None
				#++++++++++++++++++++++++++++++
				hex_dict[i] = [E,NE,NW,W,SW,SE]

		#-----------------------------------------------
		elif (i+1)%cols == 0: #right side
			#-----------------------------------------------
			if rows %2 == 0: #even row
				#++++++++++++++++++++++++++++++
				E = None
				#++++++++++++++++++++++++++++++
				# if i+cols+1 < len(hexes):
				# 	NE = hexes[i+cols+1]
				# else:
				NE = None
				#++++++++++++++++++++++++++++++
				if i+cols < len(hexes):
					NW = i+cols
				else:
					NW = None
				#++++++++++++++++++++++++++++++
				if i-1 >= 0:
					W = i-1
				else:
					W = None
				#++++++++++++++++++++++++++++++
				if i-cols >= 0:
					SW = i-cols
				else:
					SW = None
				#++++++++++++++++++++++++++++++
				# if i-cols+1 >= 0:
				# 	SE = hexes[i-cols+1]
				# else:
				SE = None
				#++++++++++++++++++++++++++++++
				hex_dict[i] = [E,NE,NW,W,SW,SE]

			#-----------------------------------------------
			elif rows %2 != 0: #odd row
				#++++++++++++++++++++++++++++++
				E = None
				#++++++++++++++++++++++++++++++
				if i+cols < len(hexes):
					NE = i+cols
				else:
					NE = None
				#++++++++++++++++++++++++++++++
				if i+cols < len(hexes):
					NW = i+cols-1
				else:
					NW = None
				#++++++++++++++++++++++++++++++
				if i-1 >= 0:
					W = i-1
				else:
					W = None
				#++++++++++++++++++++++++++++++
				if i-cols-1 >= 0:
					SW = i-cols-1
				else:
					SW = None
				#++++++++++++++++++++++++++++++
				if i-cols >= 0:
					SE = i-cols
				else:
					SE = None
				#++++++++++++++++++++++++++++++
				hex_dict[i] = [E,NE,NW,W,SW,SE]

		#-----------------------------------------------
		else: #general case
			#-----------------------------------------------
			if rows %2 == 0: #even row
				#++++++++++++++++++++++++++++++
				if i+1 < len(hexes):
					E = i+1
				else:
					E = None
				#++++++++++++++++++++++++++++++
				if i+cols+1 < len(hexes):
					NE = i+cols+1
				else:
					NE = None
				#++++++++++++++++++++++++++++++
				if i+cols < len(hexes):
					NW = i+cols
				else:
					NW = None
				#++++++++++++++++++++++++++++++
				if i-1 >= 0:
					W = i-1
				else:
					W = None
				#++++++++++++++++++++++++++++++
				if i-cols-1 >= 0:
					SW = i-cols
				else:
					SW = None
				#++++++++++++++++++++++++++++++
				if i-cols >= 0:
					SE = i-cols+1
				else:
					SE = None
				#++++++++++++++++++++++++++++++
				hex_dict[i] = [E,NE,NW,W,SW,SE]

			#-----------------------------------------------
			elif rows %2 != 0: #odd row
				if i+1 < len(hexes):
					E = i+1
				else:
					E = None
				#++++++++++++++++++++++++++++++
				if i+cols+1 < len(hexes):
					NE = i+cols
				else:
					NE = None
				#++++++++++++++++++++++++++++++
				if i+cols < len(hexes):
					NW = i+cols-1
				else:
					NW = None
				#++++++++++++++++++++++++++++++
				if i-1 >= 0:
					W = i-1
				else:
					W = None
				#++++++++++++++++++++++++++++++
				if i-cols-1 >= 0:
					SW = i-cols-1
				else:
					SW = None
				#++++++++++++++++++++++++++++++
				if i-cols >= 0:
					SE = i-cols
				else:
					SW = None
				#++++++++++++++++++++++++++++++
				hex_dict[i] = [E,NE,NW,W,SW,SE]
	return hex_dict