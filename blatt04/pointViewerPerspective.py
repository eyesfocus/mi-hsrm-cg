from Tkinter import *
from Canvas import *
import sys
import random
from math import *

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

def draw():
    """ draw points """
    global canonViewVolume

    # clipping
    

    # viewport-transformation
    # viewport = ?
    
    for e in viewport:
        x, y = e[0], e[1]
        p = can.create_oval(x-HPSIZE, y-HPSIZE, x+HPSIZE, y+HPSIZE,
                           fill=COLOR, outline=COLOR)
        pointList.insert(0,p)

def rotYp():
    """ rotate counterclockwise around y axis """
    angle = math.radians(20)
    rotate(angle)

    can.delete(*pointList)
    draw()

def rotYn():
    """ rotate clockwise around y axis """
    angle = -math.radians(20)
    rotate(angle)
    
    can.delete(*pointList)
    draw()

def rotate(angle):
    global canonViewVolume
    cos = cos(angle)
    sin = sin(angle)

    canonViewVolume = [[cos*point[0] + sin*point[2], point[1], -sin*point[0] + cos*point[2]] for point in canonViewVolume]

    
if __name__ == "__main__":
    #check parameters
    if len(sys.argv) != 1:
       print "pointViewerTemplate.py"
       sys.exit(-1)

    # create main window
    mw = Tk()

    # read data
    dataPoints = [map(float, line.split()) for line in file('data/cow_points.raw')]
    
    # bounding box
    boundingBox = [map(min, zip(*dataPoints)), map(max, zip(*dataPoints))]

    # center of boundingbox
    center = [(coords[0] + coords[1]) / 2.0 for coords in zip(*boundingBox)]

    ###########################
    
    # calculate smallest radius r
    radius = sqrt(sum(map(lambda x: x*x, map(lambda x,y: x-y, center, boundingBox[0])))) 
    print "radius %s" % radius

    # init camera-coords with e=(0,0,d=2r), c=(0,0,0), up=(0,1,0)
    e = [0,0,2*radius]
    c = [0,0,0]
    up = [0,1,0]

    f = map(lambda x: x/abs(2*radius), map(lambda x,y: x-y, c, e))
    s = [1,0,0] #per hand
    u = [0,1,0] #per hand
    
    # modelview-transformation (multiplicate with LookAt-Matrix)
    modelViewPoints = [[s[0]*p[0], u[1]*p[1], -f[2]*p[2]]  for p in dataPoints]    

    # view frustum transformation (multiplicate with Perspective Transformation Matrix)
    near = radius
    far = 2*radius
    angle = radians(30)
    cot = cos(angle)/sin(angle)
    aspect = WIDTH/float(HEIGHT)

    #canonViewVolume = [[cot/aspect * p[0], cot * p[1], (-(far+near)/(far-near) * p[2]) + (-(2*far*near)/(far-near))] for p in modelViewPoints]
    
    ############################
    
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
    # draw()

    # start
    mw.mainloop()
    
