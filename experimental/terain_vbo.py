import pygame
from OpenGL.GL import *
from ctypes import *

import numpy as np


def init_vertices():
    X = np.arange(-50, 50)
    Y = np.arange(-50, 50)
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X ** 2 + Y ** 2)
    Z = np.sin(R)

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

    triangles = np.array(triangles)

    return triangles


def update_z(progress, triangles):
    triangles[:, 2] = np.sin(progress * (np.sqrt(triangles[:, 0] ** 2 + triangles[:, 1] ** 2)))


vertices = init_vertices().flatten()
# vertices = [3,0,0,4,1,0,3,1,0]#vertices[:3]
# vertices = [1, 0, 0, 1, 1, 0, 0, 2, 0]  # vertices[:3]
# result = {ndarray: (9,)} [3 0 0 4 1 0 3 1 0]...View as Array
pygame.init()

screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF, 24)
glViewport(0, 0, 800, 600)
glClearColor(0.0, 0.5, 0.5, 1.0)
glEnableClientState(GL_VERTEX_ARRAY)

vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, (c_float * len(vertices))(*vertices), GL_STATIC_DRAW)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    glClear(GL_COLOR_BUFFER_BIT)
    glRotatef(-1, 0, 1, 0)

    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glVertexPointer(3, GL_FLOAT, 0, None)

    glDrawArrays(GL_POLYGON, 0, len(vertices))

    pygame.display.flip()
