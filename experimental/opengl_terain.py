import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np


def get_vertices(progress):
    X = np.arange(-5, 5, 0.5)
    Y = np.arange(-5, 5, 0.5)
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X ** 2 + Y ** 2)
    Z = np.sin(R * progress)

    xy_points = np.array(list(zip(X.flatten(), Y.flatten())))

    from scipy.spatial import Delaunay
    tri = Delaunay(xy_points)
    xx = X.flatten()[tri.simplices]
    yy = Y.flatten()[tri.simplices]
    zz = Z.flatten()[tri.simplices]
    triangles = []
    for t in zip(xx, yy, zz):
        t_points = list(zip(*t))
        triangles.extend(t_points)
    return triangles, np.max(Z), np.min(Z)


def draw(progress):
    vertices, max_z, min_z = get_vertices(progress)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glBegin(GL_POLYGON)
    for ver in vertices:
        glColor3f(ver[2]/(max_z-min_z)+0.1, 0, 1-ver[2]/(max_z-min_z)+0.1)
        glVertex3fv(ver)
    glEnd()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -15)

    rotation_speed = 2
    camera_distance = 10

    progress = 0.1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()  # checking pressed keys
        if keys[pygame.K_UP]:
            glRotatef(-rotation_speed, camera_distance, 0, 0)
        if keys[pygame.K_DOWN]:
            glRotatef(rotation_speed, camera_distance, 0, 0)
        if keys[pygame.K_LEFT]:
            glRotatef(rotation_speed, 0, camera_distance, 0)
        if keys[pygame.K_RIGHT]:
            glRotatef(-rotation_speed, 0, camera_distance, 0)
        if keys[pygame.K_1]:
            progress += 0.01

        draw(progress)
        pygame.display.flip()
        pygame.time.wait(10)


main()
