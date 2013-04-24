# -*- coding: utf-8 -*-

from algebra import Point, Vector

class Light(object):
    '''Pointlight of a Scene'''
    
    def __init__(self, lightpoint, colora = (1, 1, 1), colorin = (1, 1, 1)):
        self.point = lightpoint
        self.ca = Vector(colora)
        self.cin = Vector (colorin)
    
    def __repr__(self):
        return "Light(point: %s, ca: %s, cin: %s)" % (repr(self.point), repr(self.ca), repr(self.cin))
