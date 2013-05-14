import math

class HomVec3(object):
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.coords = (self.x, self.y, self.z, self.w)

    def isVector(self):
        return self.w == 0

    def length(self):
        assert self.isVector()
        return math.sqrt(self.x**2+self.y**2+self.z**2)

    def getPoint(self):
        xx = self.x / self.w
        yy = self.y / self.w
        zz = self.z / self.w
        ww = self.w / self.w
        return HomVec3(xx, yy, zz, ww)

    def __mod__(self, s):
        if type(s) == HomVec3:
            xx = self.y*s.z - self.z*s.y
            yy = self.z*s.w - self.w*s.z
            zz = self.w*s.x - self.x*s.w
            ww = self.x*s.y - self.y*s.x
            return HomVec3(xx, yy, zz, ww)

    def __add__(self, s):
        xx = self.x + s.x
        yy = self.y + s.y
        zz = self.z + s.z
        ww = self.w + s.w
        return HomVec3(xx, yy, zz, ww)
    
    def __sub__(self, s):
        xx = self.x - s.x
        yy = self.y - s.y
        zz = self.z - s.z
        ww = self.w - s.w
        return HomVec3(xx, yy, zz, ww)

    __radd__ = __add__
    __rsub__ = __sub__


class HomVec2(object):
    def __init__(self, x, y, w):
        self.x = x
        self.y = y
        self.w = w
        self.coords = (self.x, self.y, self.w)

    def isVector(self):
        return self.w == 0

    def length(self):
        assert self.isVector()
        return math.sqrt(self.x**2+self.y**2)

    def getPoint(self):
        xx = self.x / self.w
        yy = self.y / self.w
        ww = self.w / self.w
        return HomVec2(xx, yy, ww)

    def __mod__(self, s):
        if type(s) == HomVec2:
            xx = self.y*s.w - self.w*s.y
            yy = self.w*s.x - self.x*s.w
            ww = self.x*s.y - self.y*s.x
            return HomVec2(xx, yy, ww)

    def __add__(self, s):
        xx = self.x + s.x
        yy = self.y + s.y
        ww = self.w + s.w
        return HomVec2(xx, yy, ww)
    
    def __sub__(self, s):
        xx = self.x - s.x
        yy = self.y - s.y
        ww = self.w - s.w
        return HomVec2(xx, yy, ww)

    __radd__ = __add__
    __rsub__ = __sub__
    

    
