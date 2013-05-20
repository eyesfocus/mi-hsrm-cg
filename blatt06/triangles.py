from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
from numpy import array

import sys, math

points = []
strip = False
mode = GL_TRIANGLES


def initGL():
    glClearColor(0.0, 0.0, 1.0, 0.0)

def display():
    global vb, points
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(.75, .75, .75)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    
    vb.bind()
    glVertexPointerf(vb)
    glEnableClientState(GL_VERTEX_ARRAY)
    glDrawArrays(mode, 0, len(points))
    vb.unbind()
    glDisableClientState(GL_VERTEX_ARRAY)
    glFlush()
    
def main():
    global mode
    
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE)
    glutCreateWindow('Triangles')

    if strip:
        initTriangleStripPoints()
        mode = GL_TRIANGLE_STRIP
    else:
        initTrianglePoints()
    glutDisplayFunc(display)
    initGL()
    glutMainLoop()

def initTrianglePoints():
    global vb, points

    print 'Triangle Mode'
    
    a = 0.1
    h = .5 * math.sqrt(3) * a
    
    points.append([0.0, 0.0]) #1
    points.append([a/2.0, h]) #2
    points.append([a, 0.0]) #3

    points.append([a/2.0, h]) #2
    points.append([a, 0.0]) #3
    points.append([a + a/2.0, h]) #4

    points.append([a, 0.0]) #3
    points.append([a + a/2.0, h]) #4
    points.append([2*a, 0.0]) #5

    points.append([a/2.0+a, h]) #4
    points.append([2*a, 0.0]) #5
    points.append([2*a + a/2.0, h]) #6

    points.append([2*a, 0.0]) #5
    points.append([2*a + a/2.0, h]) #6
    points.append([3*a, 0.0]) #7

    points.append([2*a + a/2.0, h]) #6
    points.append([3*a, 0.0]) #7
    points.append([3*a + a/2.0, h]) #8

    points.append([2*a + a/2.0, h]) #6
    points.append([3*a + a/2.0, h]) #8
    points.append([3*a, 2*h]) #9

    points.append([3*a + a/2.0, h]) #8
    points.append([3*a, 2*h]) #9
    points.append([4*a, 2*h]) #10

    points.append([3*a + a/2.0, h]) #8
    points.append([4*a, 2*h]) #10
    points.append([4*a + a/2.0, h]) #11

    points.append([4*a, 2*h]) #10
    points.append([4*a + a/2.0, h]) #11
    points.append([5*a, 2*h]) #12

    points.append([4*a + a/2.0, h]) #11
    points.append([5*a, 2*h]) #12
    points.append([5*a + a/2.0, h]) #13

    points.append([5*a, 2*h]) #12
    points.append([5*a + a/2.0, h]) #13
    points.append([6*a, 2*h]) #14
    
    vb = vbo.VBO(array(points, 'f'))


def initTriangleStripPoints():
    global vb, points

    print 'Triangle Strip Mode'
    
    a = 0.1
    h = .5 * math.sqrt(3) * a
    
    points.append([0.0, 0.0]) #1
    points.append([a/2.0, h]) #2
    points.append([a, 0.0]) #3
    points.append([a + a/2.0, h]) #4
    points.append([2*a, 0.0]) #5
    points.append([2*a + a/2.0, h]) #6
    points.append([3*a, 0.0]) #7
    points.append([3*a + a/2.0, h]) #8


    points.append([2*a + a/2.0, h]) #6
    points.append([3*a, 2*h]) #9
    points.append([3*a + a/2.0, h]) #8
    points.append([4*a, 2*h]) #10
    points.append([4*a + a/2.0, h]) #11
    points.append([5*a, 2*h]) #12
    points.append([5*a + a/2.0, h]) #13
    points.append([6*a, 2*h]) #14
    
    vb = vbo.VBO(array(points, 'f'))
    

if __name__ == '__main__':
    if len(sys.argv) > 1:
        strip = True
    main()
