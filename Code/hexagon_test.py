import matplotlib.pyplot as plt
import numpy as np

def hexagon(center,size):
	x_vals = []
	y_vals = []
	for i in range(7):
		deg = (60*i)-30
		rad = deg*np.pi/180

		x_vals.append(center[0]+size*np.cos(rad))
		y_vals.append(center[1]+size*np.sin(rad))

	return x_vals,y_vals

def tile_hex(rows,cols):
	size = 1
	for i in range(rows):
		# print(i,i%2)
		for j in range(cols):
			if i%2 == 0:
				# print('even')
				center = [(j*np.sqrt(3)*size)+(np.sqrt(3)*size)/2,i*(2*size*0.75)]
			else:
				# print('odd')
				center = [(j*np.sqrt(3)*size)+(np.sqrt(3)*size)/2+(i-(i-1))*(np.sqrt(3)*size)/2,i*(2*size*0.75)]
			# print(center)
			
			x,y = hexagon(center,size)
			plt.plot(x,y)
		# print('==============')

	plt.show()

def main():
	tile_hex(5,5)

if __name__ == "__main__":
	main()