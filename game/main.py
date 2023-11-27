import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import * 
from OpenGL.GLUT import *
import sys


class Game:
    def __init__(self) -> None:
        self.display_size = (1920, 1080)
        self.cell_size = 20
        self.field = [[0 for _ in range(self.display_size[0] // self.cell_size)]
                      for _ in range(self.display_size[1] // self.cell_size)]

    def initialize(self) -> None:
        pygame.init()
        self.display = pygame.display.set_mode(self.display_size, DOUBLEBUF | OPENGL)

    def run(self) -> None:
        self.initialize()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.display.fill((255, 255, 255))
            glBegin(GL_LINES)
            for edge in edges:
                for vertex in edge:
                    glVertex3fv(vertices[vertex])
            glEnd()
            pygame.display.flip()
            pygame.time.wait(10)


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the screen and reset the color and depth buffers


# Initialize a GLUT instance which will allow us to customize our window
glutInit()
# Set the display mode to use RGB color
glutInitDisplayMode(GLUT_RGBA)
# Set the width and height of the window
glutInitWindowSize(500, 500)
# Set the position of the window on the screen
glutInitWindowPosition(0, 0)
# Give the window a title

wind = glutCreateWindow("OpenGL Graphics Window")
glutDisplayFunc(showScreen)  # Tell GLUT to call the showScreen function to continuously update the window
glutIdleFunc(showScreen)  # Draw any graphics or shapes in the showScreen function at all times
glutMainLoop()
