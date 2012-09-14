import pygame
from pygame.locals import *
import cv
import inspect
import numpy
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *

from artoolkit import *

def resize(width, height):
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(60.0, float(width)/height, .1, 1000.)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
# resize

def init():
	glEnable(GL_DEPTH_TEST)

	glShadeModel(GL_FLAT)
	glClearColor(1.0, 1.0, 1.0, 0.0)

	glEnable(GL_COLOR_MATERIAL)

	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)        
	glLight(GL_LIGHT0, GL_POSITION,  (0, 1, 1, 0))
# init

def surface_to_texture(surface):
	textureData = pygame.image.tostring(surface, "RGBA", 1)

	width = surface.get_width()
	height = surface.get_height()

	texture = glGenTextures(1)
	glBindTexture(GL_TEXTURE_2D, texture)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA,
	GL_UNSIGNED_BYTE, textureData)

	return texture, width, height
# surface_to_texture

artoolkit = ARToolKit()
size = artoolkit.size

pygame.init()
screen = pygame.display.set_mode(size, HWSURFACE|OPENGL|DOUBLEBUF)
pygame.display.set_caption('ARToolKit')

resize(*size)
init()

running = True
while running:
	for event in pygame.event.get():
		if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
			running = False
	# for

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	artoolkit.update()

	frame = numpy.asarray(artoolkit.frame, dtype=numpy.uint8).reshape(size[1], size[0], 3)
	image = cv.fromarray(frame)
	pyimage = pygame.image.frombuffer(image.tostring(), cv.GetSize(image), 'RGB')

	screen.blit(pyimage, (0, 0))

	pygame.display.flip()
# while

artoolkit.close()