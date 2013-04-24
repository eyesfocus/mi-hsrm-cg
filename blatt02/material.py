# -*- coding: utf-8 -*-

from algebra import Vector

class Material(object):
    '''Describes the Material of an Object in a Scene'''
    
    def __init__(self, color, ka = .3, kd = .6, ks = .2, small_n = 1):
        self.baseColor = color
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.small_n = small_n

    def baseColorAt(self, p):
        '''Returns the baseColor'''
        return self.baseColor

class CheckerboardMaterial(Material):
    def __init__(self):
        Material.__init__(self, Vector(1,1,1), .6, .6, .2)
        self.otherColor = Vector(0,0,0)
        self.checkSize = 1

    def baseColorAt(self, p):
        v = Vector(p)
        v.scale(1.0 / self.checkSize)
        if (int(abs(v.x) + 0.5) + int(abs(v.y) + 0.5) + int(abs(v.z) + 0.5)) % 2:
            return self.otherColor
        return self.baseColor
