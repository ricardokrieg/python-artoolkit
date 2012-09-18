import pygame
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import *

class Moon:
	def __init__(self, image):
		image = pygame.image.load(image)
		self.texture_data = pygame.image.tostring(image, "RGBA", 1)
		self.width = image.get_width()
		self.height = image.get_height()

		self.radius = 5
		self.rotation = 0
		self.translation = 0

		self.parent_radius = 50*1.5
	# __init__

	def update(self):
		self.rotation += 150/self.radius
		self.translation += 0.1

		if self.rotation >= 360: self.rotation = 0
		if self.translation >= 360: self.translation = 0
	# update

	def draw(self):
		ambient = [0.0, 0.0, 0.0, 1.0]
		flash = [0.0, 0.0, 0.0, 1.0]
		flash_shiny = [50.0]
		light_position = [100.0,-200.0,200.0,0.0]
		ambi = [0.1, 0.1, 0.1, 0.1]
		light_zero_color = [0.9, 0.9, 0.9, 0.1]

		glPushMatrix()

		glEnable(GL_TEXTURE_2D)
		glEnable(GL_LIGHTING)
		glEnable(GL_DEPTH_TEST)

		glEnable(GL_LIGHT0)
		glLightfv(GL_LIGHT0, GL_POSITION, light_position)
		glLightfv(GL_LIGHT0, GL_AMBIENT, ambi)
		glLightfv(GL_LIGHT0, GL_DIFFUSE, light_zero_color)
		glMaterialfv(GL_FRONT, GL_SPECULAR, flash)
		glMaterialfv(GL_FRONT, GL_SHININESS, flash_shiny)
		glMaterialfv(GL_FRONT, GL_AMBIENT, ambient)

		texture = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, texture)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.texture_data)

		glTranslatef(0, 0, self.parent_radius)
		glTranslatef(self.parent_radius*sin(self.translation), self.parent_radius*cos(self.translation), 0)
		glRotatef(self.rotation, 0, 0, 1)

		quadric = gluNewQuadric()
		gluQuadricNormals(quadric, GLU_SMOOTH)
		gluQuadricTexture(quadric, True)
		gluSphere(quadric, self.radius, 36, 18)

		glDisable(GL_DEPTH_TEST)
		glDisable(GL_LIGHTING)
		glDisable(GL_TEXTURE_2D)

		glPopMatrix()
	# draw
# Moon