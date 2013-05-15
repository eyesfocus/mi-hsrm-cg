from Tkinter import *
from Canvas import *
import sys


WIDTH  = 400 # width of canvas
HEIGHT = 400 # height of canvas

HPSIZE = 10 # half of point size (must be integer)
FCOLOR = "#AAAAAA" # fill color
BCOLOR = "#000000" # boundary color

pointList = []   # list of points
elementList = [] # list of elements (used by Canvas.delete(...))

swap = False


def drawGrid(s):
    """ draw a rectangular grid """
    for i in range(0,WIDTH,s):
        element = can.create_line(i,0,i,HEIGHT)
    for i in range(0,HEIGHT,s):
        element = can.create_line(0,i,WIDTH,i)


def drawPoints():
    """ draw points """
    for p in pointList:
        element = can.create_rectangle(p[0]-HPSIZE, p[1]-HPSIZE,
				       p[0]+HPSIZE, p[1]+HPSIZE,
				       fill=FCOLOR, outline=BCOLOR)
        elementList.append(element)    


def drawLines():
    """ draw lines """
    for line in zip(pointList[::2],pointList[1::2]):
        drawBresenhamLine(line[0],line[1])
        element = can.create_line(line,width=1)
        elementList.append(element)    


def drawBresenhamLine(p,q):
    """ draw a line using bresenhams algorithm """
    global elementList

    x0, y0 = p
    x1, y1 = q

    if p[0] > q[0]:
        p, q = q, p

    x0, y0 = p
    x1, y1 = q
        
    a, b = y1 - y0, x0 - x1
    
    d = 2*a + b
    IncE, IncNE = 2*a, 2*(a+b)

    if x1 == x0:
        m = float('inf')
    else:
        m = (y1-y0)/float(x1-x0)
        
    if m >= 0 and m <=1:
        x,y = x0, y0
        endX = x1
        swap = False
    else:
        x,y = y0, x0
        endX = y1
        swap = True
    
    while x < endX:
        if not swap:
            add(x,y)
        else:
            add(y,x)
            
        if d <= 0:
            d += IncE
        else:
            d += IncNE
            y += 2*HPSIZE
        x += 2*HPSIZE

            

def add(x,y):
    global elementList
    element = can.create_rectangle(x-HPSIZE, y-HPSIZE,
                                       x+HPSIZE, y+HPSIZE,
				       fill=FCOLOR, outline=BCOLOR)
       
    elementList.append(element)
    

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
    drawLines()

def clearAll():
    """ clear all (point list and canvas) """
    can.delete(*elementList)
    del pointList[:]


def mouseEvent(event):
    """ process mouse events """
    # get point coordinates
    d = 2*HPSIZE
    p = [d/2+d*(event.x/d), d/2+d*(event.y/d)] 
    pointList.append(p)
    draw()


if __name__ == "__main__":
    #check parameters
    if len(sys.argv) != 1:
       print "draw lines using bresenhams algorithm"
       sys.exit(-1)

    # create main window
    mw = Tk()
    mw._root().wm_title("Line drawing using bresenhams algorithm")

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

    drawGrid(2*HPSIZE)
    # start
    mw.mainloop()
    
