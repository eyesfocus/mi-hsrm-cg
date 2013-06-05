# -*- coding: utf-8 -*-
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.arrays import vbo
from numpy import *
from math import *
from itertools import *

import sys, os

objects = dict(COW='data/cow.obj', ELEPHANT='data/elephant.obj', BUNNY='data/bunny.obj', SQUIRREL='data/squirrel.obj')

WIDTH, HEIGHT = 500, 500

RED = [1.,0.,0.,0.]
GREEN = [0.,1.,0.,0.]
BLUE = [0.,0.,1.,0.]
YELLOW = [1.,1.,0.,0.]
BLACK = [0.,0.,0.,0.]
WHITE = [1.,1.,1.,1.]

colors = [BLACK, WHITE, RED, GREEN, BLUE, YELLOW]

ROTATION_ANGLE = .1  # angle for keyboard-rotation
X_AXIS = [1.,0.,0.]
Y_AXIS = [0.,1.,0.]
Z_AXIS = [0.,0.,1.]

MAX_ZOOM = 1.5
MIN_ZOOM = 0.5
INIT_ZOOM = 1.0   

CAMERA_Z = 4      # position of camera
PLANE = 1.5

## KEYS:
##    ESC:     exit programm
##
##    x, X:    rotate (anti-)clockwise on x-axis
##    y, Y:    rotate (anti-)clockwise on y-axis
##    z, Z:    rotate (anti-)clockwise on z-axis
##    c:       change color of object
##    C:       change backgroundcolor
##    p:       switch between othogonal and central perspective
##
##
## MOUSE CLICK
##
##    left:    rotate object on arcball
##    middle:  zoom in and out
##    right:   move object

class PointCloud(object):
    def __init__(self, filename):
        self.filename = filename
        self.data = []
        self.setUpData() #inits self.vb
        self.initGeometry() #inits self.center and self.scale
        
        self.central_projection = False
        self.actOri = matrix(
                [[1, 0, 0, 0],
                 [0, 1, 0, 0],
                 [0, 0, 1, 0],
                 [0, 0, 0, 1]])
        self.axis = X_AXIS
        self.angle = 0
        self.position = 0, 0, 0
        self.zoom = INIT_ZOOM
        self.color = 2

    def setUpData(self):   
        geoData = file(self.filename).readlines()
   
        self.vertices = [map(float, line.split()[1:]) for line in geoData if line.startswith('v ')]
        self.normals = [line.split()[1:] for line in geoData if line.startswith('vn')]
        faces = [line.split()[1:] for line in geoData if line.startswith('f')]
   
        for face in faces:
           for f in face:
              if '/' in f:
                 tmp = [part if part != '' else -1 for part in f.split('/')]
                 vn, nn = int(tmp[0])-1, int(tmp[2])-1
                 self.data.append(self.vertices[vn])# + normals[nn]) comment in if you wanna have normals
              else:
                 tmp = [part for part in f.split()]
                 vn = int(tmp[0])-1
                 self.data.append(self.vertices[vn])

        self.vb = vbo.VBO(array(self.data, 'f'))

    def initGeometry(self):
        # bounding box
        boundingBox = [map(min, zip(*self.vertices)), map(max, zip(*self.vertices))]

        # center of bounding box
        self.center = [(coords[0] + coords[1]) / 2.0 for coords in zip(*boundingBox)]

        # find longest side and calculate scale (for length = 2.0)
        self.scale = 2.0 / max([(coords[1] - coords[0]) for coords in zip(*boundingBox)])

    def draw(self):
        glColor(*colors[self.color])       #object color

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        self.vb.bind() # load points
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointerf(self.vb)

        glLoadIdentity()
        gluLookAt(0,0,CAMERA_Z, 0,0,0, 0,1,0) # update camera
        glTranslatef(*self.position) # move to specific position
        glMultMatrixf(self.actOri * rotate(self.angle, self.axis)) #rotate
        glScale(self.scale, self.scale, self.scale) # scale so that boundingbox has a length of 2
        glTranslatef(-self.center[0], -self.center[1], -self.center[2]) # move to center

        glDrawArrays(GL_TRIANGLES, 0, len(self.data))
        self.vb.unbind()
        glDisableClientState(GL_VERTEX_ARRAY)

    def rotate(self, angle, axis):
       c, mc = cos(angle), 1-cos(angle)
       s = sin(angle)
       l = sqrt(dot(array(axis), array(axis)))
       x, y, z = array(axis) / l
       r = matrix(
          [[x*x*mc+c, x*y*mc-z*s, x*z*mc+y*s, 0],
           [x*y*mc+z*s, y*y*mc+c, y*z*mc-x*s, 0],
           [x*z*mc-y*s, y*z*mc+x*s, z*z*mc+c, 0],
           [0, 0, 0, 1]])
       return r.transpose()

    def doArcBall(self, angle, axis):
        pass # do stuff you do with actOri = actOri * rotate(blaaaa)


def reset():
   global doRotation, doDrag, doZoom
   global current_bg

   doRotation, doDrag, doZoom = False, False, False
   current_bg = 5



def init(width, height):
   """ Initialize an OpenGL window """
   glClearColor(*colors[current_bg])         #background color
   updateProjection()
   
       
def display():
   """ Render all objects"""
   global model
   glClearColor(*colors[current_bg])      #background color   
   glClear(GL_COLOR_BUFFER_BIT)           #clear screen

   model.draw()

   
   glutSwapBuffers() 


def updateProjection():
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
   if model.central_projection:
      showCentral(WIDTH, HEIGHT)
   else:
      showOrtho(WIDTH, HEIGHT)
   glMatrixMode(GL_MODELVIEW)
   

def showCentral(width, height):
   fieldofview = 40*model.zoom
   gluPerspective(fieldofview, width/float(height), CAMERA_Z - PLANE, CAMERA_Z + PLANE)


def showOrtho(width, height):
   zoomedPlane = PLANE*model.zoom
   
   if width <= height:
       glOrtho(-zoomedPlane, zoomedPlane,
               -zoomedPlane*height/width, zoomedPlane*height/width,
               CAMERA_Z - PLANE, CAMERA_Z + PLANE)
   else:
       glOrtho(-zoomedPlane*width/height, zoomedPlane*width/height,
               -zoomedPlane,zoomedPlane,
               CAMERA_Z - PLANE, CAMERA_Z + PLANE)


def reshape(width, height):
   """ adjust projection matrix to window size"""
   global WIDTH, HEIGHT
   WIDTH, HEIGHT = width, height
   glViewport(0, 0, width, height)
   updateProjection()
   glutPostRedisplay()


def rotate(angle, axis):
   c, mc = cos(angle), 1-cos(angle)
   s = sin(angle)
   l = sqrt(dot(array(axis), array(axis)))
   x, y, z = array(axis) / l
   r = matrix(
      [[x*x*mc+c, x*y*mc-z*s, x*z*mc+y*s, 0],
       [x*y*mc+z*s, y*y*mc+c, y*z*mc-x*s, 0],
       [x*z*mc-y*s, y*z*mc+x*s, z*z*mc+c, 0],
       [0, 0, 0, 1]])
   return r.transpose()
   

def projectOnSphere(x, y, r):
   x, y = x - WIDTH/2.0, HEIGHT/2.0 - y
   a = min(r*r, x*x, y*y)
   z = sqrt(r*r - a)
   l = sqrt(x*x + y*y + z*z)
   return x/l, y/l, z/l



def keyPressed(key, x, y):
    global current_bg, model

    if key == chr(27):
        sys.exit()

    if key in 'xXyYzZcCp0M':
        # rotation
        if key == 'x':
            model.actOri = model.actOri * rotate(ROTATION_ANGLE, X_AXIS)
        if key == 'X':
            model.actOri = model.actOri * rotate(-ROTATION_ANGLE, X_AXIS)
        if key == 'y':
            model.actOri = model.actOri * rotate(ROTATION_ANGLE, Y_AXIS)
        if key == 'Y':
            model.actOri = model.actOri * rotate(-ROTATION_ANGLE, Y_AXIS)
        if key == 'z': 
            model.actOri = model.actOri * rotate(ROTATION_ANGLE, Z_AXIS)
        if key == 'Z':
            model.actOri = model.actOri * rotate(-ROTATION_ANGLE, Z_AXIS)
         
        # color switch
        if key == 'C':
            current_bg = current_bg+1 if current_bg < len(colors)-1 else 0
        if key == 'c':
            model.color = model.color+1 if model.color < len(colors)-1 else 0

        # perspective switch
        if key == 'p':
            model.central_projection = not model.central_projection
            updateProjection()
         
        # model switch
        if key == 'M':
            model = modelcycle.next()
            
        # reset
        if key == '0':
            reset()
            updateProjection()
        glutPostRedisplay()
   

def mousebuttonpressed(button, state, x, y):
   """ handle mouse events """
   global startPoint, actOri, angle
   global doRotation, doDrag, doZoom

   r = min(WIDTH, HEIGHT)/ 2.0
   
   if button == GLUT_LEFT_BUTTON:
      if state == GLUT_DOWN:
         doRotation = True
         startPoint = projectOnSphere(x, y, r)
      if state == GLUT_UP:
         doRotation = False
         model.actOri = model.actOri * rotate(model.angle, model.axis)
         model.angle = 0
         
   if button == GLUT_RIGHT_BUTTON:
      if state == GLUT_DOWN:
         startPoint = x, y
         doDrag = True
      if state == GLUT_UP:
         doDrag = False

   if button == GLUT_MIDDLE_BUTTON:
      if state == GLUT_DOWN:
         startPoint = y
         doZoom = True
      if state == GLUT_UP:
         doZoom = False


def mousemoved(x,y):
   """ handle mouse motion """
   global startPoint
   global angle, axis, scale
   global dragX, dragY, zoom
   
   if doRotation:
      r = min(WIDTH, HEIGHT)/ 2.0
      movePoint = projectOnSphere(x, y, r)
      model.angle = acos(dot(startPoint, movePoint))
      model.axis = cross(startPoint, movePoint)
      glutPostRedisplay()

   if doDrag:
      xBefore, yBefore = startPoint
      dragX = model.position[0] + float(x - xBefore) / float(WIDTH) * 2 * PLANE * model.zoom
      dragY = model.position[1]  - float(y - yBefore) / float(HEIGHT) * 2 * PLANE * model.zoom
      model.position = dragX, dragY, 0
      startPoint = (x, y)
      glutPostRedisplay()         
      
   if doZoom: 
      if startPoint < y:
         zoom = zoom - 0.1 if zoom > MIN_ZOOM else zoom
      if startPoint > y:
         zoom = zoom + 0.1 if zoom < MAX_ZOOM else zoom
      startPoint = y
      updateProjection()
      glutPostRedisplay()
      

def initModels():
    global modelcycle, model
    models = []
    models.append(PointCloud(objects['ELEPHANT']))
    models.append(PointCloud(objects['COW']))
    models.append(PointCloud(objects['BUNNY']))
    models.append(PointCloud(objects['SQUIRREL']))
 
    modelcycle = cycle(models)
    model = modelcycle.next()

 
def initOpenGL():
    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow("sple openGL/GLUT template")

    glutDisplayFunc(display)            #register display function
    glutReshapeFunc(reshape)            #register reshape function
    glutKeyboardFunc(keyPressed)        #register keyboard function 
    glutMouseFunc(mousebuttonpressed)   #register mouse function
    glutMotionFunc(mousemoved)          #register motion function

    init(WIDTH, HEIGHT) # initialize OpenGL state
    glutMainLoop() #start even processing
   


if __name__ == "__main__":
    initModels()
    reset()
    initOpenGL()
