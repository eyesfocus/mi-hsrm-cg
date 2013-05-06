from Tkinter import *
from Canvas import *
import sys

WIDTH  = 400 # width of canvas
HEIGHT = 400 # height of canvas

HPSIZE = 2 # half of point size (must be integer)
CCOLOR = "#0000FF" # blue

elementList = [] # list of elements (used by Canvas.delete(...))

polygon = [[50,50],[350,50],[350,350],[50,350],[50,50]]
polygon_a = []
polygon_z = []

time = 0
dt = 0.01

def drawObjekts():
    """ draw polygon and points """
    # TODO: inpterpolate between polygons and render
    for (p,q) in zip(polygon,polygon[1:]):
        elementList.append(can.create_line(p[0], p[1], q[0], q[1],
                                           fill=CCOLOR))
        elementList.append(can.create_oval(p[0]-HPSIZE, p[1]-HPSIZE,
                                           p[0]+HPSIZE, p[1]+HPSIZE,
                                           fill=CCOLOR, outline=CCOLOR))
            
def quit(root=None):
    """ quit programm """
    if root==None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()


def draw():
    """ draw elements """
    can.delete(*elementList)
    del elementList[:]
    drawObjekts()
    can.update()


def forward():
    global time, polygon
    while(time<1):
        time += dt
        # TODO: interpolate 
        polygon = interpolate()
        print time
        draw()


def backward():
    global time, polygon
    while(time>0):
        time -= dt
        # TODO: interpolate 
        polygon = interpolate()
        print time
        draw()

def interpolate():
    return map(lambda a,b: (a[0]+b[0], a[1]+ b[1]), polygon_a, [(time*x[0], time*x[1]) for x in map(lambda p,q: (q[0]-p[0],q[1]-p[1]), polygon_a, polygon_z)])
    

if __name__ == "__main__":
    # check parameters
    if len(sys.argv) != 3:
       print "morph.py firstPolygon secondPolygon"
       sys.exit(-1)

    # TODOS:
    # - read in polygons
    file_a = file("polygonA.dat")
    file_z = file("polygonZ.dat")
    
    polygon_z = [(float(y[0]),float(y[1])) for y in [tuple(x.split()) for x in [lines.strip() for lines in file_z.readlines()]]]
    polygon_a = [(float(y[0]),float(y[1])) for y in [tuple(x.split()) for x in [lines.strip() for lines in file_a.readlines()]]]

    # - transform from local into global coordinate system
    polygon_a = [(y[0]*WIDTH, -y[1]*HEIGHT+HEIGHT) for y in polygon_a]
    polygon_z = [(y[0]*WIDTH, -y[1]*HEIGHT+HEIGHT) for y in polygon_z]
    
    # - make both polygons contain same number of points
    if min(len(polygon_z), len(polygon_a)) == len(polygon_z):
        while len(polygon_z) != len(polygon_a):
            polygon_z.append(polygon_z[0])
    else:
        while len(polygon_z) != len(polygon_a):
            polygon_z.append(polygon_z[0])
        polygon_a.append(polygon_a[0])

    polygon = polygon_a

    # create main window
    mw = Tk()
    mw._root().wm_title("Morphing")

    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.pack()
    cFr = Frame(mw)
    cFr.pack(side="left")
    bClear = Button(cFr, text="backward", command=backward)
    bClear.pack(side="left")
    bClear = Button(cFr, text="forward", command=forward)
    bClear.pack(side="left")
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()
    draw()
    
    # start
    mw.mainloop()
    
    
