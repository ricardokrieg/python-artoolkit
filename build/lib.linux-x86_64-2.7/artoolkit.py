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

frame = cv.CreateImage(artoolkit.size, cv.IPL_DEPTH_8U, 4)
# frame = cv.CreateMat(artoolkit.size[0], artoolkit.size[1], cv.CV_8UC4)

while True:
	screen.fill((0, 0, 0))

	artoolkit.update()

	x = cv.fromarray(numpy.asarray(artoolkit.frame))
	print x

	image = pygame.image.frombuffer(frame.tostring(), cv.GetSize(frame), 'RGB')
	screen.blit(image, (0, 0))

	pygame.display.flip()
# while

artoolkit.close()