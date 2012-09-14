import pygame
from pygame.locals import *
import cv
import inspect
import numpy

from artoolkit import *

artoolkit = ARToolKit()

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('ARToolKit')

cv.NamedWindow('Camera')

while True:
	screen.fill((0, 0, 0))

	artoolkit.update()

	frame = numpy.asarray(artoolkit.frame, dtype=numpy.uint8).reshape(480, 640, 3)
	image = cv.fromarray(frame)
	pyimage = pygame.image.frombuffer(image.tostring(), cv.GetSize(image), 'RGB')
	screen.blit(pyimage, (0, 0))

	pygame.display.flip()
# while

artoolkit.close()