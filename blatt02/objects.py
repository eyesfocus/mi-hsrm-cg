import math

from algebra import Vector


class Object(object):
    '''Object in the scene'''
    def __init__(self, surface):
        self.surface = surface

    def intersectionParameter(self, ray):
        return None

    def normalAt(self, p):
        return self.normal

    def baseColorAt(self, point):
        return self.surface.baseColorAt(point)

    def calcColor(self, light, lightray, ray, point):
        '''Calculates the color with Phong-Model'''
        
        ka = self.surface.ka
        kd = self.surface.kd
        ks = self.surface.ks
        baseColor = self.surface.baseColorAt(point.coords)
        small_n = self.surface.small_n

        n = self.normalAt(point)
        d = ray.direction
        l = lightray.direction
        lr = l.reflected(n) * -1
        
        cin = light.cin
        ca = light.ca
        
        ambient = baseColor * ca * ka 
        diffuse = Vector(0,0,0)
        specular = Vector(0,0,0)
        
        specdot = lr.dot(d.scale(-1))
        diffdot = l.dot(n)
        
        if diffdot > 0:
            diffuse = baseColor * cin * kd * diffdot
        if specdot > 0:
            specular = baseColor * cin * ks * specdot**small_n
                        
        return ambient + diffuse + specular



class Sphere(Object):
    def __init__(self, center, radius, surface):
        Object.__init__(self, surface)
        self.center = center # point
        self.radius = radius # scalar

    def __repr__(self):
        return 'Sphere(%s,%s)' % (repr(self.center), self.radius)

    def intersectionParameter(self, ray):
        co = self.center - ray.origin
        v = co.dot(ray.direction)
        discriminant = v*v - co.dot(co) + self.radius*self.radius
        if discriminant < 0:
            return None
        else:
            return v - math.sqrt(discriminant)

    def normalAt(self, p):
        return (p - self.center).normalized()

        
class Plane(Object):
    def __init__(self, point, normal, surface):
        Object.__init__(self, surface)
        self.point = point # point
        self.normal = normal.normalized() # vector
            
    def __repr__(self):
        return 'Plane(%s,%s)' % (repr(self.point), repr(self.normal))

    def intersectionParameter(self, ray):
        op = ray.origin - self.point
        a = op.dot(self.normal)
        b = ray.direction.dot(self.normal)
        if b:
            return -a/b
        else:
            return None


class Triangle(Object):
    def __init__(self, a, b, c, surface):
        Object.__init__(self, surface)

        self.a = a # point
        self.b = b # point
        self.c = c # point
        self.u = self.b - self.a # direction vector
        self.v = self.c - self.a # direction vector

    def __repr__(self):
        return 'Triangle(%s,%s,%s)' % (repr(self.a), repr(self.b), repr(self.c))

    def intersectionParameter(self, ray):
        w = ray.origin - self.a
        dv = ray.direction.cross(self.v)
        dvu = dv.dot(self.u)
        if dvu == 0.0:
            return None
        wu = w.cross(self.u)
        r = dv.dot(w) / dvu
        s = wu.dot(ray.direction) / dvu
        if 0<=r and r<=1 and 0<=s and s<=1 and r+s <=1:
            return wu.dot(self.v) / dvu
        else:
            return None
         
    def normalAt(self, p):
        return self.u.cross(self.v).normalized()
