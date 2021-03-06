from ray import Ray
from algebra import *

import math

BACKGROUND_COLOR = Vector(0, 0, 0)

class Scene(object):
    def __init__(self, wRes, hRes):
        self.objectlist = []
        self.wRes = wRes
        self.hRes = hRes

    def addObject(self, obj):
        '''Add Object to a Scene'''
        self.objectlist.append(obj)

    def addLight(self, light):
        '''Add Light to a Scene'''
        self.light = light

    def setUpCamera(self, e, up, c, fieldofview):
        '''Calculate Coordinates of the Camera'''

        self.e = e
        self.up = up
        self.c = c

        self.fieldofview = math.radians(fieldofview)

        self.f = (c-e).normalized()
        self.s = self.f.cross(up).normalized()
        self.u = self.s.cross(self.f) * -1 

        #Aufloesung
        ratio = float(self.wRes) / float(self.hRes)
        alpha = self.fieldofview / 2.0

        # Groesse Abbildungsbereich
        self.height = 2.0 * math.tan(alpha) 
        self.width = ratio * self.height

        # Pixelgroesse
        self.pixelWidth = self.width / (self.wRes-1)
        self.pixelHeight = self.height / (self.hRes-1)

    def render(self, image, level=0):
        '''Renders Scene pixelwise'''
        
        self.maxlevel = level
        print 'Rendering with recursion depth = %d ...' %level
        for x in range(self.wRes):
            for y in range(self.hRes):
                ray = self.calcRay(x,y)
                color = self.traceRay(0, ray)                           
                image.putpixel((x,y), tuple(map(int, color.scale(255).coords))) #TODO rgb       

    def traceRay(self, level, ray):
        hitPointData = self.intersect(ray)
        if hitPointData:
            return self.shade(level, hitPointData)
        return BACKGROUND_COLOR

    def intersect(self, ray):
        '''Test if theres any intersection'''
        
        maxdist = float('inf')
        nearestObject = None
        
        for obj in self.objectlist:
            hitdist = obj.intersectionParameter(ray)
            if hitdist < maxdist and hitdist > 0.000001:
                maxdist = hitdist
                nearestObject = obj
        if nearestObject:
            point = ray.pointAtParameter(maxdist)
            return (nearestObject, point, ray) # intersection
        else:
            return 0 # no intersection

    def shade(self, level, hitPointData):
        '''Set pixelcolor'''

        obj, point, ray = hitPointData

        # calculate own color
        directColor = self.calcColor(hitPointData)

        if level == self.maxlevel:
            return directColor
        
        # calculate reflected color
        reflectedRay = self.computeReflectedRay(hitPointData)
        reflectedColor = self.traceRay(level+1, reflectedRay)
        reflection = obj.surface.reflection#ks

        return directColor + reflectedColor * reflection

    def computeReflectedRay(self, hitPointData):
        '''Computes reflected ray'''
        obj, point, ray = hitPointData
        
        n = obj.normalAt(point)
        dr = ray.direction.reflected(n)
        return Ray(point, dr)

    def calcRay(self, x, y):
        '''Calculate ray with x- and y-coords of screen'''
        
        xcomp = self.s.scale(x*self.pixelWidth - self.width/2.0)
        ycomp = self.u.scale(y*self.pixelHeight - self.height/2.0)
        return Ray(self.e, self.f + xcomp + ycomp)

    def inShadow(self, obj, lightray):
        '''Tests if the object is blocked by another''' 
        for otherobj in self.objectlist:
            if otherobj is not obj:
                hitdist = otherobj.intersectionParameter(lightray)
                if hitdist > 0.00001:
                    return True # in shadow
        return False # not in shadow

    def calcColor(self, hitPointData):
        '''Calculate Pixelcolor'''
        obj, point, ray = hitPointData

        lightray = Ray(point, self.light.point - point)

        inShadow = self.inShadow(obj, lightray)
        
        if not inShadow: # add direct light
            color = obj.calcColor(self.light, lightray, ray, point)
        else: # add ambient light
            color = self.light.ca * obj.surface.ka * obj.baseColorAt(point.coords)
        return color
