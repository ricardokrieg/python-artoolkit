import pygame
from pygame.locals import *
import cv
import numpy

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

#from artoolkit import *

#artoolkit = ARToolKit()
#size = artoolkit.size
size = (640, 480)

pygame.init()
screen = pygame.display.set_mode(size, HWSURFACE|OPENGL|DOUBLEBUF)
pygame.display.set_caption('ARToolKit')

glClearColor(1, 1, 1, 1)

running = True
while running:
	for event in pygame.event.get():
		if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
			running = False
	# for

	#artoolkit.update()

	#frame = numpy.asarray(artoolkit.frame, dtype=numpy.uint8).reshape(size[1], size[0], 3)
	#image = cv.fromarray(frame)
	#pyimage = pygame.image.frombuffer(image.tostring(), cv.GetSize(image), 'RGB')

	glClear(GL_COLOR_BUFFER_BIT)

	#glViewport(320, 0, 320, 240)

	glColor3f(1, 0, 0)
	glBegin(GL_TRIANGLES)
	glVertex3f(-0.5, -0.5, 0)
	glVertex3f(0, 0.5, 0)
	glVertex3f(0.5, -0.5, 0)
	glEnd()

	pygame.display.flip()
# while

#artoolkit.close()