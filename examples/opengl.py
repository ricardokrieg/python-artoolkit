#!/usr/bin/python

import pygame
from pygame.locals import *
import cv
import inspect
import numpy
from math import *

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from artoolkit import *

def draw_surface(surface):
	glMatrixMode(GL_PROJECTION)
	glPushMatrix()
	glLoadIdentity()
	glOrtho(0, 1, 0, 1, 0, 1)

	glMatrixMode(GL_MODELVIEW)
	glPushMatrix()
	glLoadIdentity()

	glDepthMask(False)
	glEnable(GL_TEXTURE_2D)

	textureData = pygame.image.tostring(surface, "RGBA", 1)
	width = surface.get_width()
	height = surface.get_height()
	texture = glGenTextures(1)
	glBindTexture(GL_TEXTURE_2D, texture)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

	glBegin(GL_QUADS)
	glTexCoord2d(0, 0)
	glVertex2f(0, 0)
	glTexCoord2d(1, 0)
	glVertex2f(1, 0)
	glTexCoord2d(1, 1)
	glVertex2f(1, 1)
	glTexCoord2d(0, 1)
	glVertex2f(0, 1)
	glEnd()

	glDepthMask(True)
	glDisable(GL_TEXTURE_2D)

	glPopMatrix()
	glMatrixMode(GL_PROJECTION)
	glPopMatrix()
	glMatrixMode(GL_MODELVIEW)
# draw_surface

pygame.init()
screen = pygame.display.set_mode((640, 480), HWSURFACE|OPENGL|DOUBLEBUF)
pygame.display.set_caption('ARToolKit')
glutInit()

artoolkit = ARToolKit()
size = artoolkit.size

running = True
while running:
	for event in pygame.event.get():
		if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE: running = False
	# for

	artoolkit.update()

	glClear(GL_COLOR_BUFFER_BIT)
	glColor3f(1, 1, 1)
	
	# frame = numpy.asarray(artoolkit.frame, dtype=numpy.uint8).reshape(size[1], size[0], 3)
	# image = cv.fromarray(frame)
	# pyimage = pygame.image.frombuffer(image.tostring(), cv.GetSize(image), 'RGB')

	# artoolkit.draw2d()
	artoolkit.draw3d()

	glColor3f(1, 0, 0)
	glTranslatef( 0.0, 0.0, 25.0 )
	glutSolidTeapot(30)

	pygame.display.flip()
# while

artoolkit.close()