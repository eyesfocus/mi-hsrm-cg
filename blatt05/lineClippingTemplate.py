from Tkinter import *
from Canvas import *
import sys


WIDTH  = 700 # width of canvas
HEIGHT = 700 # height of canvas

HPSIZE = 3 # half of point size (must be integer)
CLSIZE = 4 # clip line size
FCOLOR = "#000000" # black (fill color)
BCOLOR = "#000000" # blue (boundary color)

clipRegion = [] # clipping rectangle

pointList = []   # list of points
elementList = [] # list of elements (used by Canvas.delete(...))


class Point:
    """ Point consists of coordinates and region code """
    def __init__(self, co, cr):
        self.coords = co
        # region code 
        self.reCode = 8*(co[1]<cr[1][1])+4*(co[1]>cr[0][1])+2*(co[0]>cr[1][0])+(co[0]<cr[0][0])


def normalizeClipRegion(clipRegion):
    """ normalize clip region to point list [lower left, upper right] """
    ll = map(min,apply(zip,clipRegion)) # lower left corner
    ur = map(max,apply(zip,clipRegion)) # upper right corner
    return [[ll[0],ur[1]], [ur[0],ll[1]]]


def drawPoints():
    """ draw oints """
    for p in pointList:
        element = can.create_oval(p.coords[0]-HPSIZE, p.coords[1]-HPSIZE,
                                  p.coords[0]+HPSIZE, p.coords[1]+HPSIZE,
                                  fill=FCOLOR, outline=BCOLOR)
        elementList.append(element)    


def drawBox():
    """ use first and second point in pointlist to draw a box"""
    if len(pointList) >1:
        element = can.create_rectangle(pointList[0].coords,pointList[1].coords, width=3)
        elementList.append(element)   

    
def drawLines():
    """ use third and next points in pointlist to draw lines"""
    for line in zip(pointList[2::2],pointList[3::2]):
        lc = lineCase(line)
        if lc == 0:
            print "line complete inside rectangle!"
            element = can.create_line(line[0].coords, line[1].coords, width=CLSIZE)
            elementList.append(element)
        elif lc == -1:
            print "line not visible!"
            element = can.create_line(line[0].coords, line[1].coords, width=1)
            elementList.append(element)
        else:
            print "need further tests... linecode: ", lc
            element = can.create_line(line[0].coords, line[1].coords, width=1)
            elementList.append(element)
            newLine = calcNewLine(line, lc, clipRegion)
            if newLine:
                element = can.create_line(newLine[0].coords, newLine[1].coords, width=CLSIZE)
                elementList.append(element)

def lineCase(line):
    """ Cohen-Sutherland Algorithm. Use region codes of line points to determine wether
        1. both points -> line lies completly inside the clipping region
	2. both points -> line lies complety on one side of the clipping region
	3. Otherwise """
    union = line[0].reCode | line[1].reCode
    sect  = line[0].reCode & line[1].reCode

    # 2. case
    if sect != 0:
	# line is completly unvisible
        return -1
    # 1. and 3. case
    if union == 0: # line is completly visible
        return 0
    else:
        # othervise furhter tests are nessecary
        return union
	
    
def calcNewLine(line, lc, clipRegion):
    """ Calculate clipped line """
    # TODO: calculate new line (clipped at clipRegion)

    minmax = [map(min, zip(*clipRegion)), map(max, zip(*clipRegion))]
    minx, miny, maxx, maxy = minmax[0][0],  minmax[0][1],  minmax[1][0], minmax[1][1]

    newLine = []

    if lc & 1:
        # Bit 0 = 1: intersect with minx
        y = intersectedY(line, minx)
        np = Point([minx,y], clipRegion)
        if np.reCode == 0:
          newLine.append(np) if np.reCode == 0
    if lc & 2:
        # Bit 1 = 1: intersect with maxx
        y = intersectedY(line, maxx)
        np = Point([maxx,y], clipRegion)
        if np.reCode == 0:
            newLine.append(np)
    if lc & 4:
        # Bit 2 = 1: intersect with maxy
        x = intersectedX(line, maxy)
        np = Point([x,maxy], clipRegion)
        if np.reCode == 0:
            newLine.append(np)
    if lc & 8:
        # Bit 3 = 1: intersect with miny
        x = intersectedX(line, miny)
        np = Point([x, miny], clipRegion)
        if np.reCode == 0:
            newLine.append(np)

    if len(newLine) == 1: # point is half inside, half outside. find 2nd point of new line
        pointOne, pointTwo = line[0], line[1]
        newLine.append(pointOne) if pointOne.reCode == 0 else newLine.append(pointTwo)
        
    return newLine


def intersectedY(line, x):
    x1, y1, x2, y2 = line[0].coords[0],  line[0].coords[1],  line[1].coords[0], line[1].coords[1]
    return ((y2-y1)/float(x2-x1))*(x-x1) + y1

def intersectedX(line, y):
    x1, y1, x2, y2 = line[0].coords[0],  line[0].coords[1],  line[1].coords[0], line[1].coords[1]
    return ((x2-x1)/float(y2-y1))*(y-y1) + x1


def quit(root=None):
    """ quit programm """
    if root==None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()


def draw():
    """ draw elements """
    can.delete(*elementList)
    drawPoints()
    drawBox()
    drawLines()


def clearAll():
    """ clear all (point list and canvas) """
    can.delete(*elementList)
    del pointList[:]


def mouseEvent(event):
    """ process mouse events """
    #print "left mouse button clicked at ", event.x, event.y
    global clipRegion
    p = [event.x, event.y]
    if len(pointList) < 2: 
        point = Point(p, [[0,0],[WIDTH,HEIGHT]])
    elif len(pointList) == 2:
        clipRegion = normalizeClipRegion([pointList[0].coords, pointList[1].coords])
        point = Point(p, clipRegion)
    else:
        point = Point(p, clipRegion)
    pointList.append(point)
    draw()


if __name__ == "__main__":
    #check parameters
    if len(sys.argv) != 1:
       print "LineClipping"
       sys.exit(-1)

    # create main window
    mw = Tk()
    mw._root().wm_title("Line clipping (Cohen-Sutherland Algorithm)")

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
    
