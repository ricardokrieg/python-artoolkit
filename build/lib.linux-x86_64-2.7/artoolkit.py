# import pygame
# from pygame.locals import *
# import cv

from artoolkit import *

artoolkit = ARToolKit()

# pygame.init()
# screen = pygame.display.set_mode(artoolkit.size)
# pygame.display.set_caption('ARToolKit')

# device = cv.CreateCameraCapture(0)

while True:
	# screen.fill((0, 0, 0))

	artoolkit.update()
	print artoolkit.frame

	# frame = cv.QueryFrame(device)
	# cv.CvtColor(frame, frame, cv.CV_BGR2RGB)
	# frame = pygame.image.frombuffer(frame.tostring(), cv.GetSize(frame), 'RGB')

	# screen.blit(frame, (0, 0))

	# pygame.display.flip()
# while

artoolkit.close()