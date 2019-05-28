import numpy as numpy

def line_equ(pt1 , pt2):
	# finds the equation of the line connecting two points in the form ay+bx+c=0
	x1,y1 = pt1
	x2,y2 = pt2
	a = y2 - y1
	b = x2 - x1
	c = b*x1 - a*y1 
	return (-a,b,c)

def line_dist(line_equ,pt1):
	# finds the perpedicular distance from a line to a point
	x,y = pt1
	a,b,c = line_equ
	d = np.abs(a*x+b*y+c)/np.sqrt(a**2 + b**2)
	return d

def find_exits(nodes,xc,yc)
	xc = 0
	yc = 0
	# initilize nonlinear portions of the equations
	right = l*np.sin(2*np.pi/3)
	up = l*np.cos(2*np.pi/3)
	# calculate the six corners
	pt1 = (xc,yc+l)
	pt2 =  (xc+right,yc+up)
	pt3 = (xc+right,yc-up)
	pt4 = (xc,yc-l)
	pt5 = (xc-right,yc-up)
	pt6 = (xc-right,yc+up)
	# finds equations of the lines connecting the points
	lines = [line_equ(pt1,pt2),line_equ(pt2,pt3),line_equ(pt3,pt4),line_equ(pt4,pt5),line_equ(pt5,pt6),line_equ(pt6,pt1)]
	#calculates the distances between each point and line
	distances = np.zeros(len(nodes),6)
	for i in range(len(nodes)):
		for j in range(6):
			x = nodes[i].x
			y = nodes[i].y
			distances[i,j] = line_dist(lines[j],(x,y))

	exit = np.zeros((6,1))
	# finds the minimum distance for each line
	for i in range(6):
		exit[i] = nodes[np.amin(distances[:,i],1)]
	
	return exit


