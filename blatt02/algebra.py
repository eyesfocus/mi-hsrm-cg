# -*- coding: utf-8 -*-

import math

class Vector(object):
    '''Vector in R3'''
    
    def __init__(self, x, y=0, z=0):
        if(type(x) == tuple):
            self.coords = x
        else:
            self.coords = (x,y,z)
        self.coords = tuple(map(float, self.coords))
        (self.x, self.y, self.z) = self.coords
                
    def __repr__(self):
        return "Vector(%s, %s, %s)" % (repr(self.x), repr(self.y), repr(self.z))

    def __eq__(self, other):
        return self.coords == other.coords

    def __mul__(self, other):
        if type(other) == Vector:
            vec = tuple(map(lambda x: x[0]*x[1], zip(self.coords, other.coords)))
        else:
            vec = tuple(map(lambda x: x*other, self.coords))
        return Vector(vec)

    def __div__(self, s):
        vec = tuple(map(lambda x: x/s, self.coords))
        return Vector(vec)

    def __add__(self, other):
        vec = tuple(map(lambda x: x[0]+x[1], zip(self.coords, other.coords)))
        return Vector(vec)

    def __sub__(self, other):
        vec = tuple(map(lambda x: x[0]-x[1], zip(self.coords, other.coords)))
        return Vector(vec)

    def scale(self, scalar):
        return self * scalar

    def length(self):
        return math.sqrt(sum(map(lambda x: x**2, self.coords)))

    def normalized(self):
        return self/self.length()

    def dot(self, other):
        return sum(map(lambda x: x[0]*x[1], zip(self.coords, other.coords)))

    def cross(self, other):
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y  *other.x
        return Vector(x,y,z)

    def reflected(self, n):
        return self - n * 2 * self.dot(n)


class Point(object):
    '''Punkt in R3'''
    
    def __init__(self, x, y=0, z=0):
        if(type(x)==tuple):
            self.coords = x
        else:
            self.coords = (x, y, z)
        self.coords = tuple(map(float, self.coords))
        (self.x, self.y, self.z) = self.coords
        
    def __repr__(self):
        return "Point(%s, %s, %s)" % (repr(self.x), repr(self.y), repr(self.z))

    def __eq__(self, other):
        return other.coords == self.coords

    def __sub__(self, other):
        vec = tuple(map(lambda x: x[0]-x[1], zip(self.coords, other.coords)))
        return Vector(vec)

    def __add__(self, vec):
        point = tuple(map(lambda x: x[0]+x[1], zip(self.coords, vec.coords)))
        return Point(point)




