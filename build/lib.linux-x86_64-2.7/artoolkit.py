from artoolkit import *

artoolkit = ARToolKit()

while True:
	artoolkit.update()

	print artoolkit.matrix
# while

artoolkit.close()