import pygame
from OpenGL.GL import *
from ctypes import *

from pyglet.gl import gluPerspective

pygame.init()
display = (800, 600)
screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF, 24)
glViewport(0, 0, 800, 600)
glClearColor(0.0, 0.5, 0.5, 1.0)

glEnableClientState(GL_VERTEX_ARRAY)
glEnableClientState(GL_COLOR_ARRAY)

vertices = [-1, -1, 1, 1, -1, 1, 1, 1, 1, -1, 1, 1,
            -1, -1, -1, -1, 1, -1, -1, 1, 1, -1, -1, 1,
            -1, -1, -1, 1, -1, -1, 1, -1, 1, -1, -1, 1,
            -1, -1, -1, 1, -1, -1, 1, 1, -1, -1, 1, -1,
            1, -1, -1, 1, 1, -1, 1, 1, 1, 1, -1, 1,
            -1, 1, -1, 1, 1, -1, 1, 1, 1, -1, 1, 1
            ]
vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, (c_float * len(vertices))(*vertices), GL_STATIC_DRAW)

gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

glTranslatef(0.0, 0.0, -5)

running = True
while running:

    keys = pygame.key.get_pressed()  # checking pressed keys
    rotation_speed = 0.1
    if keys[pygame.K_UP]:
        glRotatef(rotation_speed, 1, 0, 0)
    if keys[pygame.K_DOWN]:
        glRotatef(-rotation_speed, 1, 0, 0)
    if keys[pygame.K_LEFT]:
        glRotatef(rotation_speed, 0, 1, 0)
    if keys[pygame.K_RIGHT]:
        glRotatef(-rotation_speed, 0, 1, 0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glClear(GL_COLOR_BUFFER_BIT)

    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glVertexPointer(3, GL_FLOAT, 0, None)
    glColorPointer(3, GL_FLOAT, 0, None)

    glDrawArrays(GL_POLYGON, 0, 24)

    pygame.display.flip()

glDisableClientState(GL_COLOR_ARRAY);
glDisableClientState(GL_VERTEX_ARRAY);
