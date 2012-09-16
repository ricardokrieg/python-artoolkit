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

def resize(width, height):
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(60.0, float(width)/height, .1, 1000.)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
# resize

def init():
	glutInit()
	glEnable(GL_DEPTH_TEST)

	glShadeModel(GL_FLAT)
	glClearColor(1.0, 1.0, 1.0, 0.0)

	glEnable(GL_COLOR_MATERIAL)

	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)        
	glLight(GL_LIGHT0, GL_POSITION,  (0, 1, 1, 0))

	gluLookAt(0,0,10, 0,0,0, 0,1,0)
# init

def draw_surface(surface):
	glEnable(GL_TEXTURE_2D)

	surface = pyimage
	textureData = pygame.image.tostring(surface, "RGBA", 1)
	width = surface.get_width()
	height = surface.get_height()
	texture = glGenTextures(1)
	glBindTexture(GL_TEXTURE_2D, texture)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

	glBegin(GL_QUADS)
	glColor3f(1, 1, 1)

	glTexCoord2d(0, 0)
	glVertex3f(-7.7, -7.7, 0)
	glTexCoord2d(1, 0)
	glVertex3f(7.7, -7.7, 0)
	glTexCoord2d(1, 1)
	glVertex3f(7.7, 7.7, 0)
	glTexCoord2d(0, 1)
	glVertex3f(-7.7, 7.7, 0)

	glEnd()

	glDisable(GL_TEXTURE_2D)
# draw_surface

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

	glLoadIdentity()

	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

	artoolkit.update()

	frame = numpy.asarray(artoolkit.frame, dtype=numpy.uint8).reshape(size[1], size[0], 3)
	image = cv.fromarray(frame)
	pyimage = pygame.image.frombuffer(image.tostring(), cv.GetSize(image), 'RGB')

	draw_surface(pyimage)

	if artoolkit.gl_matrix[0][0] > 0:
		glMatrixMode(GL_MODELVIEW)
		glLoadMatrixd(artoolkit.gl_matrix)
	# if
	color = [1.0, 0., 0., 1.]
	glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
	glutSolidSphere(2, 20, 20)

	pygame.display.flip()
# while

artoolkit.close()