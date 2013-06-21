from Tkinter import *
from Canvas import *
import sys

WIDTH  = 400 # width of canvas
HEIGHT = 400 # height of canvas

HPSIZE = 2 # half of point size (must be integer)
CCOLOR = "#0000FF" # blue (color of control-points and polygon)

BCOLOR = "#000000" # black (color of bezier curve)
BWIDTH = 2 # width of bezier curve

pointList = []   # list of (control-)points
elementList = [] # list of elements (used by Canvas.delete(...))
bezierList = []


def drawPoints(points, color):
    """ draw (control-)points """
    for p in points:
        element = can.create_oval(p[0]-HPSIZE, p[1]-HPSIZE,
                                  p[0]+HPSIZE, p[1]+HPSIZE,
                                  fill=color, outline=color)
        elementList.append(element)    

def drawPolygon(points, color):
    """ draw (control-)polygon conecting (control-)points """
    if len(points) > 1:
        for i in range(len(points)-1):
            element = can.create_line(pointList[i][0], pointList[i][1],
                                      pointList[i+1][0], pointList[i+1][1],
                                      fill=color)
            elementList.append(element)

def drawBezierCurve():
    """ draw bezier curve defined by (control-)points """
    if len(pointList) <= 2:
        return
    bezierList = []
    bezierList.append(pointList[0])
    N = 100
    for i in range(1, N + 1):
        t = i/float(N + 1)
        bezierList.append(doCasteljau(pointList, t))
    bezierList.append(pointList[-1])
    
    drawPoints(bezierList, BCOLOR)
    drawPolygon(bezierList, BCOLOR)

def doCasteljau(points, t):
    if len(points) == 1:
        return points[0]
    nextpoints = []

    pl = [(points[i], points[i+1]) for i in range(len(points)) if i < len(points)-1] #list of current and next point
    
    for (start, end) in pl:
        p = (start[0]+t*(end[0]-start[0]), start[1]+t*(end[1]-start[1]))
        nextpoints.append(p)
        
    return doCasteljau(nextpoints, t)


def quit(root=None):
    """ quit programm """
    if root==None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()


def draw():
    """ draw elements """
    can.delete(*elementList)
    drawPoints(pointList, CCOLOR)
    drawPolygon(pointList, CCOLOR)
    drawBezierCurve()


def clearAll():
    """ clear all (point list and canvas) """
    can.delete(*elementList)
    del pointList[:]


def mouseEvent(event):
    """ process mouse events """
    print "left mouse button clicked at ", event.x, event.y
    pointList.append([event.x, event.y])
    draw()


if __name__ == "__main__":
    #check parameters
    if len(sys.argv) != 1:
       print "pointViewerTemplate.py"
       sys.exit(-1)

    # create main window
    mw = Tk()

    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.bind("<Button-1>",mouseEvent)
    can.pack()
    cFr = Frame(mw)
    cFr.pack(side="left")
    bClear = Button(cFr, text="Clear", command=clearAll)
    bClear.pack(side="left")
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()

    # start
    mw.mainloop()
    
