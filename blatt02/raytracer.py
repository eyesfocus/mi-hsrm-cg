# -*- coding: utf-8 -*-
from PIL import Image

from scene import Scene
from objects import Sphere, Plane, Triangle
from algebra import Vector, Point
from light import Light
from material import Material, CheckerboardMaterial

import sys, time

WIDTH = 320
HEIGHT = 240

RADIUS = 2.
FIELDOFVIEW = 45

if __name__ == '__main__':
    beginTime = time.time()
    
    recursionLevel = 0
    
    if len(sys.argv) == 2:
        recursionLevel = int(sys.argv[1])
    if len(sys.argv) > 2:
        print 'raytracer.py takes only 1 argument: recursion levelssss'
        sys.exit()
        
    image = Image.new('RGB', (WIDTH, HEIGHT))

    scene = Scene(WIDTH, HEIGHT)

    # Colors
    red = Vector(1, 0, 0)
    green = Vector(0, 1, 0)
    blue = Vector(0, 0, 1)
    yellow = Vector(1, 1, 0)
    grey = Vector(.5, .5, .5)

    # Materials
    redSurface = Material(red)
    greenSurface = Material(green)
    blueSurface = Material(blue)
    greySurface = Material(grey)
    yellowSurface = Material(yellow)
    checkerboard = CheckerboardMaterial() 

    # Add objects to scene
    scene.addObject(Sphere(Point(2.5, 3, -10), RADIUS, redSurface))
    scene.addObject(Sphere(Point(-2.5, 3, -10), RADIUS, greenSurface))
    scene.addObject(Sphere(Point(0, 7, -10), RADIUS, blueSurface))
    scene.addObject(Plane(Point(0, 0, 0), Vector(0, 1, 0), checkerboard))# greySurface))
    scene.addObject(Triangle(Point(2.5, 3, -10), Point(-2.5, 3, -10), Point(0, 7, -10), yellowSurface))

    scene.addLight(Light(Point(30, 30, 10)))

    scene.setUpCamera(Point(0,2,10), Vector(0,1,0), Point(0,3,0), FIELDOFVIEW)

    # and render
    scene.render(image, level=recursionLevel)
    
    print 'Rendering Time: %d seconds' % (time.time() - beginTime)
    
    image.show()
    image.save('out_image.png', 'PNG')
