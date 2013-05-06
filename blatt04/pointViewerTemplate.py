from Tkinter import *
from Canvas import *
import sys
import random
import math

WIDTH  = 400 # width of canvas
HEIGHT = 400 # height of canvas

HPSIZE = 1 # double of point size (must be integer)
COLOR = "#0000FF" # blue

NOPOINTS = 1000

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

    # clip z-coordinate
    points2d = [point[:2] for point in canonViewVolume]

    # viewport transformation
    viewport = [[(point[0] + 1) * WIDTH/2.0, (1 - point[1]) * HEIGHT/2.0] for point in points2d]

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
    cos = math.cos(angle)
    sin = math.sin(angle)

    canonViewVolume = [[cos*point[0] + sin*point[2], point[1], -sin*point[0] + cos*point[2]] for point in canonViewVolume]

    
if __name__ == "__main__":
    #check parameters
    if len(sys.argv) != 1:
       print "pointViewerTemplate.py"
       sys.exit(-1)

    # create main window
    mw = Tk()

    # read data
    dataPoints = [map(float, line.split()) for line in file('data/elephant_points.raw')]

    # bounding box
    boundingBox = [map(min, zip(*dataPoints)), map(max, zip(*dataPoints))]

    # center of bounding box
    center = [(coords[0] + coords[1]) / 2.0 for coords in zip(*boundingBox)]

    # move center of bounding box to origin
    canonViewVolume = [[point[0] - center[0], point[1] - center[1], point[2] - center[2]] for point in dataPoints]

    # find longest side and calculate scale (for length = 2.0)
    sideScale = 2.0 / max([(coords[1] - coords[0]) for coords in zip(*boundingBox)])

    # scale canonViewVolume to a length of 2.0
    canonViewVolume = [[point[0]*sideScale, point[1]*sideScale, point[2]*sideScale] for point in canonViewVolume]


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
    
