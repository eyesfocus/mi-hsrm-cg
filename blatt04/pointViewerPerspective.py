from Tkinter import *
from Canvas import *
import sys
import random
import math
import numpy

WIDTH  = 400 # width of canvas
HEIGHT = 400 # height of canvas

HPSIZE = 1 # double of point size (must be integer)
COLOR = "#0000FF" # blue

pointList = [] # list of points (used by Canvas.delete(...))


def quit(root=None):
    """ quit programm """
    if root==None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()

def perspectiveTransform(point, radius):
    angle = math.radians(30)
    cot = math.cos(angle) / math.sin(angle)
    aspect = WIDTH/float(HEIGHT)
    near = 1
    far = 3
    
    a = numpy.matrix([[cot / aspect, 0, 0, 0],
                      [0, cot, 0, 0],
                      [0, 0, -(far + near) / (far - near), -2 * far * near / (far - near)],
                      [0, 0, -1, 0]])
    b = numpy.matrix([[x] for x in point])
    res = (a * b).tolist()
    return [res[0][0], res[1][0], res[2][0], res[3][0]]

def lookAtTransform(point, radius):
    a = numpy.matrix([[1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 1, -2*radius],
                      [0, 0, 0, 1]])
    b = numpy.matrix([[x] for x in point])
    res = (a * b).tolist()
    return [res[0][0], res[1][0], res[2][0], res[3][0]]


def draw():
    """ draw points """
    global transformedPoints, center, boundingBox
    
    radius = math.sqrt(sum(map(lambda x: x*x, map(lambda x,y: x-y, center, boundingBox[0])))) 

    modelViewPoints = map(lambda x: lookAtTransform(x, radius), transformedPoints)
    canonViewPoints = map(lambda x: perspectiveTransform(x, radius), modelViewPoints)

    perspectivelyDivided = [[point[0]/point[3], point[1]/point[3], point[1]/point[3], 1.] for point in canonViewPoints]

    points2d = [point[:2] for point in perspectivelyDivided]

    # clip z-coordinate
    viewport = [[(point[0] + 1) * WIDTH/2.0, (1 - point[1]) * HEIGHT/2.0] for point in points2d]
    
    for e in viewport:
        x, y = e[0], e[1]
        p = can.create_oval(x-HPSIZE, y-HPSIZE, x+HPSIZE, y+HPSIZE,
                           fill=COLOR, outline=COLOR)
        pointList.insert(0,p)

def rotYp():
    """ rotate counterclockwise around y axis """
    global transformedPoints
    
    angle = math.pi * 20. / 180
    transformedPoints = map(lambda x: rotate(x, angle), transformedPoints)

    can.delete(*pointList)
    draw()

def rotYn():
    """ rotate clockwise around y axis """
    global transformedPoints
    
    angle = -math.pi * 20. / 180
    transformedPoints = map(lambda x: rotate(x, angle), transformedPoints)

    can.delete(*pointList)
    draw()

def rotate(point, angle):
    cos = math.cos(angle)
    sin = math.sin(angle)

    a = numpy.matrix([[cos, 0, -sin, 0],
                      [0, 1, 0, 0],
                      [sin, 0, cos, 0],
                      [0, 0, 0, 1]])
    b = numpy.matrix([[x] for x in point])
    res = (a * b).tolist()
    return [res[0][0], res[1][0], res[2][0], res[3][0]]

    
if __name__ == "__main__":
    #check parameters
    if len(sys.argv) != 1:
       print "pointViewerTemplate.py"
       sys.exit(-1)

    # create main window
    mw = Tk()

    # read data
    dataPoints = [map(float, line.split()+[1.]) for line in file('data/squirrel_points.raw')]

    # bounding box
    boundingBox = [map(min, zip(*dataPoints)), map(max, zip(*dataPoints))]

    # center of bounding box
    center = [(coords[0] + coords[1]) / 2.0 for coords in zip(*boundingBox)]

    # find longest side and calculate scale (for length = 2.0)
    sideScale = 2.0 / max([(coords[1] - coords[0]) for coords in zip(*boundingBox)])

    # move center of bounding box to origin and scale to a length of 2.0
    transformedPoints = [[(point[0] - center[0])*sideScale, (point[1] - center[1])*sideScale, (point[2] - center[2])*sideScale, 1.*sideScale] for point in dataPoints]
    
    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.pack()
    bFr = Frame(mw)
    bFr.pack(side="left")
    bRotYn = Button(bFr, text="<-", command=rotYn)
    bRotYn.pack(side="left")
    bRotYp = Button(bFr, text="->", command=rotYp)
    bRotYp.pack(side="left")
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()

    # draw points
    draw()

    # start
    mw.mainloop()
    
