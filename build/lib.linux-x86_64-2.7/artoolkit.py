import pygame
from pygame.locals import *
import cv
import inspect
import numpy
from math import *

from artoolkit import *

artoolkit = ARToolKit()
size = artoolkit.size

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('ARToolKit')

font = pygame.font.SysFont(None, 36)

running = True
while running:
	for event in pygame.event.get():
		if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
			running = False
	# for

	screen.fill((0, 0, 0))

	artoolkit.update()
	matrix = artoolkit.matrix
	gl_matrix = artoolkit.gl_matrix

	print "%3.1f %3.1f %3.1f %3.1f \n\
%3.1f %3.1f %3.1f %3.1f\n\
%3.1f %3.1f %3.1f %3.1f\n\
%3.1f %3.1f %3.1f %3.1f\n" % (
		gl_matrix[0][0], gl_matrix[0][1], gl_matrix[0][2], gl_matrix[0][3], 
		gl_matrix[1][0], gl_matrix[1][1], gl_matrix[1][2], gl_matrix[1][3], 
		gl_matrix[2][0], gl_matrix[2][1], gl_matrix[2][2], gl_matrix[2][3], 
		gl_matrix[3][0], gl_matrix[3][1], gl_matrix[3][2], gl_matrix[3][3], 
	)

	frame = numpy.asarray(artoolkit.frame, dtype=numpy.uint8).reshape(size[1], size[0], 3)
	image = cv.fromarray(frame)
	pyimage = pygame.image.frombuffer(image.tostring(), cv.GetSize(image), 'RGB')

	screen.blit(pyimage, (0, 0))

	pos = artoolkit.pos
	x = int(pos[0])
	y = int(pos[1])

	angle = asin(gl_matrix[0][0])

	try:
		pygame.draw.line(screen, (255, 0, 0), (x, y), (x+50*gl_matrix[0][1], y-50*gl_matrix[0][0]), 3)
		pygame.draw.line(screen, (0, 0, 255), (x, y), (x+50*gl_matrix[0][0], y+50*gl_matrix[0][1]), 3)
		pygame.draw.circle(screen, (0, 255, 0), (x, y), 5)
	except: pass

	pygame.display.flip()
# while

artoolkit.close()