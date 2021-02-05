import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


def Cube():
    glEnable(GL_DEPTH_TEST);
    glDepthFunc(GL_LESS);

    glBegin(GL_POLYGON)
    glColor3fv((1, 0, 0.5))
    glVertex3fv((-1, -1, 1))
    glVertex3fv((1, -1, 1))
    glVertex3fv((1, 1, 1))
    glVertex3fv((-1, 1, 1))
    glEnd()

    glBegin(GL_POLYGON)
    glColor3fv((0, 0, 1))
    glVertex3fv((-1, -1, -1))
    glVertex3fv((-1, 1, -1))
    glVertex3fv((-1, 1, 1))
    glVertex3fv((-1, -1, 1))
    glEnd()

    glBegin(GL_POLYGON)
    glColor3fv((1, 0, 1))
    glVertex3fv((-1, -1, -1))
    glVertex3fv((1, -1, -1))
    glVertex3fv((1, -1, 1))
    glVertex3fv((-1, -1, 1))
    glEnd()

    glBegin(GL_POLYGON)
    glColor3fv((0.2, 0.5, 0.5))
    glVertex3fv((-1, -1, -1))
    glVertex3fv((1, -1, -1))
    glVertex3fv((1, 1, -1))
    glVertex3fv((-1, 1, -1))
    glEnd()

    glBegin(GL_POLYGON)
    glColor3fv((1, 0, 0))
    glVertex3fv((1, -1, -1))
    glVertex3fv((1, 1, -1))
    glVertex3fv((1, 1, 1))
    glVertex3fv((1, -1, 1))
    glEnd()

    glBegin(GL_POLYGON)
    glColor3fv((1, 1, 1))
    glVertex3fv((-1, 1, -1))
    glVertex3fv((1, 1, -1))
    glVertex3fv((1, 1, 1))
    glVertex3fv((-1, 1, 1))
    glEnd()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print("Left")
            if event.key == pygame.K_RIGHT:
                print("Rights")

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -5)

    def redraw():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)

    rotation_speed = 2
    while True:
        keys = pygame.key.get_pressed()  # checking pressed keys
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
        redraw()


main()
