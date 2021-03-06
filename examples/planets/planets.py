#!/usr/bin/python

import pygame
from pygame.locals import *
import cv
import inspect
import numpy
from math import *
from xml.dom.minidom import *

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from artoolkit import *
from planet import Planet
from moon import Moon

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

artoolkit_init(640, 480, '/dev/video0', 'Data/camera_para.dat')
size = artoolkit_size()

pygame.init()
screen = pygame.display.set_mode(size, HWSURFACE|OPENGL|DOUBLEBUF)
pygame.display.set_caption('ARToolKit')
glutInit()

planets = []

dom = parse('planets.xml')
xmlplanets = dom.getElementsByTagName('planet')
for xmlplanet in xmlplanets:
	texture = "img/%s" % xmlplanet.getAttribute('texture')
	pattern = "Data/%s" % xmlplanet.getAttribute('pattern')
	radius = int(xmlplanet.getAttribute('radius'))

	planet = Planet(texture, str(pattern), radius)

	for moon in xmlplanet.childNodes:
		if moon.__class__.__name__ == 'Element':
			moon_texture = "img/%s" % moon.getAttribute('texture')
			planet.add_moon(Moon(moon_texture))
		# if
	# for

	planets.append(planet)
# for

running = True
while running:
	for event in pygame.event.get():
		if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE: running = False
	# for

	next_frame()

	glClear(GL_COLOR_BUFFER_BIT)
	glColor3f(1, 1, 1)
	
	frame = numpy.asarray(artoolkit_frame(), dtype=numpy.uint8).reshape(size[1], size[0], 3)
	image = cv.fromarray(frame)
	pyimage = pygame.image.frombuffer(image.tostring(), cv.GetSize(image), 'RGB')
	draw_surface(pyimage)

	load_projection_matrix()

	for planet in planets:
		planet.update()

		planet.artoolkit.update()
		if planet.artoolkit.visible:
			planet.artoolkit.load_matrix()
			planet.draw()
		# if
	# for

	pygame.display.flip()
# while

artoolkit_close()