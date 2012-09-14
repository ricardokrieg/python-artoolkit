import pygame
from pygame.locals import *
import cv
import inspect
import numpy

from artoolkit import *

artoolkit = ARToolKit()

pygame.init()
screen = pygame.display.set_mode(artoolkit.size)
pygame.display.set_caption('ARToolKit')

running = True
while running:
	for event in pygame.event.get():
		if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
			running = False
	# for

	screen.fill((0, 0, 0))

	artoolkit.update()

	frame = numpy.asarray(artoolkit.frame, dtype=numpy.uint8).reshape(artoolkit.size[1], artoolkit.size[0], 3)
	image = cv.fromarray(frame)
	pyimage = pygame.image.frombuffer(image.tostring(), cv.GetSize(image), 'RGB')

	screen.blit(pyimage, (0, 0))

	x = artoolkit.matrix[2][0]
	if x != 0:
		print x
		pygame.draw.rect(screen, (255, 0, 0), (x*640, 0, 10, 10))
	# if

	pygame.display.flip()
# while

artoolkit.close()