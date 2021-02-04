import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

t = np.linspace(-10, 10, 1000)


def generate_sin(freq, z):
    verticies = np.array(list(zip(t, np.sin(freq * t), np.zeros_like(t) + z)))
    return verticies


def Plot(verts):
    glBegin(GL_LINES)
    for vertex in verts:
        glVertex3fv(vertex)
    glEnd()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 2, 100.0)

    glTranslatef(0.0, 0.0, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Plot(generate_sin(10, 2))
        Plot(generate_sin(20, 3))
        pygame.display.flip()
        pygame.time.wait(10)


main()
