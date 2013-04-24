from algebra import Vector

import math

class Color(Vector):
    def __init__(self, x, y=0, z=0):
        Vector.__init__(self, x, y, z)

    def toRGB(self):
        return tuple(map(lambda x: int(x*255), self.coords))
        
v = Vector(1,1,1)
c = Color(2,2,2)

print c + c
print c * 2

print c.cross(c)
