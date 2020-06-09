import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from light_bulb import Camera, Controls, Lighting

import math
import numpy as np

curve = np.array([
    [2, 2, 0], [1, 1, 0], [1, -1, 0], [2, -2, 0]
])

black_down_tip = np.array([
    [1, -1, 0], [1, -.9, 0], [2, -.1, 0]
])

gray_base = np.array([
    [2, -.1, 0], [3, 1, 0],
    # dashed
    [2.8, 1.2, 0], [3, 1.4, 0],
    [2.8, 1.6, 0], [3, 1.8, 0],
    [2.8, 2., 0], [3, 2.2, 0],
    [2.8, 2.4, 0], [3, 2.6, 0],
    # end part
    [3, 3, 0]
])

ctrlpoints = [
    [[-5, -1., -5], [0., -1., -10], [5, -1., -5]],
    [[-7.5, -1., -2.5], [0., 5, -10], [7.5, -1., -2.5]],

    [[-7.5, -1, 0], [0., 30, 0], [7.5, -1, 0]],  # center

    [[-7.5, -1., 2.5], [0., 5, 10], [7.5, -1., 2.5]],
    [[-5., -1., 5], [0., -1., 10], [5, -1., 5]],
]

glass_part = np.array([
    [3, 3, 0], [3.5, 4, 0], [3.52, 4.1, 0], [3.54, 4.2, 0],
    [3.54, 6, 0], [3.8, 6.5, 0], [7.2, 10, 0]
])

cubeColor = [0.5, 0.5, 1.0]
cubeSpecular = [1.0, 1.0, 1.0]


def opengl_init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    glMap2f(GL_MAP2_VERTEX_3, 0, 1, 0, 1, ctrlpoints)
    glEnable(GL_MAP2_VERTEX_3)
    glEnable(GL_AUTO_NORMAL)
    glMapGrid2f(20, 0.0, 1.0, 20, 0.0, 1.0)


def get_dist_xz(p):
    d = math.sqrt(p[0] * p[0] + p[2] * p[2])
    return d


def surface_revolution(curve, n_slices, cubeColor=None):
    n_points = len(curve)

    vertices = np.zeros(n_slices * n_points * 3).reshape(n_slices, n_points, 3)

    for islice in range(n_slices):
        for ipoint in range(n_points):
            r = get_dist_xz(curve[ipoint])
            z = r * math.sin(2 * math.pi * islice / n_slices)
            x = r * math.cos(2 * math.pi * islice / n_slices)
            y = curve[ipoint][1]

            vertices[islice][ipoint][0] = x
            vertices[islice][ipoint][1] = y
            vertices[islice][ipoint][2] = z

    glPushMatrix()
    for islice in range(n_slices):
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, cubeColor)
        glBegin(GL_QUAD_STRIP)
        glColor3f(*cubeColor)
        if islice == n_slices - 1:
            next_slice = 0
        else:
            next_slice = islice + 1

        for ipoint in range(n_points):
            glVertex3f(vertices[islice][ipoint][0], vertices[islice][ipoint][1],
                       vertices[islice][ipoint][2])
            glVertex3f(vertices[next_slice][ipoint][0], vertices[next_slice][ipoint][1],
                       vertices[next_slice][ipoint][2])
        glEnd()
    glPopMatrix()


def draw_top_part():
    glPushMatrix()
    glColor3f(1, 1, 0.878)
    glTranslatef(0, 11, 0)
    glEvalMesh2(GL_FILL, 0, 20, 0, 20)
    glPopMatrix()


def draw_surface(controls: Controls):
    glPushMatrix()

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, cubeColor)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, cubeSpecular)
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 10.0)

    glTranslatef(*controls.translate_vector)
    glScale(.7, .7, .7)
    # black base
    surface_revolution(black_down_tip, 100, (0, 0, 0))
    # gray base
    surface_revolution(gray_base, 100, (0.431, 0.431, 0.431))
    # glass part
    surface_revolution(glass_part, 100, (1, 1, 0.878))
    # top part
    draw_top_part()
    glPopMatrix()


def draw_sphere(translate=None):
    # draw a sphere right on where light is, helps debug :)
    glPushMatrix()
    glColor3f(0, 0, 0)

    if translate:
        glTranslatef(*translate)

    q = gluNewQuadric()
    gluQuadricDrawStyle(q, GLU_FILL)
    gluQuadricNormals(q, GLU_SMOOTH)
    gluSphere(q, .7, 50, 50)
    glPopMatrix()


def draw_sphere_onctrl():
    for seq in ctrlpoints:
        for p in seq:
            draw_sphere(translate=p)


def event_capture_loop(controls):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            controls.handle_key(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            controls.orbital_control(event.button)


def main():
    # camera vars
    eye = (0, 0, 15)
    target = (0, 0, 0)
    up = (0, 1, 0)

    pygame.init()
    display = (1600, 900)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # base settings
    glClearColor(0.761, 0.773, 0.824, 1.)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    lighting = Lighting()
    lighting.set_lighting()

    # set perspective
    gluPerspective(45, (display[0] / display[1]), .1, 50.0)
    camera = Camera(eye, target, up)
    controls = Controls(camera)
    controls.translate_vector = [0, -2, 0]

    while True:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)
        glPushMatrix()

        camera.set_look_at()
        lighting.set_lighting_position()

        opengl_init()

        draw_surface(controls)

        event_capture_loop(controls)

        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(33)


if __name__ == '__main__':
    main()
