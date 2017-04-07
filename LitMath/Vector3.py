import math
import Util

class Vector3(object):
    __slots__ = ['x', 'y', 'z']
    __hash__ = None
    
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z
        
    def set(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        return self
        
    def __copy__(self):
        return self.__class__(self.x, self.y, self.z)
    copy = __copy__
    
    def __repr__(self):
        return 'Vector3(%.2f, %.2f, %.2f)' % (self.x, self.y, self.z)
        
    def __eq__(self, other):
        if isinstance(other, Vector3):
            return Util.isEqual(self.x, other.x) and \
                   Util.isEqual(self.y, other.y) and \
                   Util.isEqual(self.z, other.z)
        else:
            return False
            
    def __ne__(self, other):
        return not self.__eq__(other)
        
    def __nonzero__(self):
        return self.x != 0 or self.y != 0 or self.z != 0
               
    def isZero(self):
        return self.x == 0 and self.y == 0 and self.z == 0
        
    def __len__(self):
        return 3
        
    def __getitem__(self, key):
        assert type(key) in (int, long)
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == 2:
            return self.z
        elif key == -1:
            return self.z
        elif key == -2:
            return self.y
        elif key == -3:
            return self.x
        else:
            raise IndexError, "Vector3 index out of range"
        
    def __setitem__(self, key, value):
        assert type(key) in (int, long)
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.z = value
        elif key == -1:
            self.z = value
        elif key == -2:
            self.y = value
        elif key == -3:
            self.x = value
        else:
            raise IndexError, "Vector3 index out of range"
        
    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def __getattr__(self, name):
        try:
            return tuple([(self.x, self.y, self.z)['xyz'.index(c)] \
                          for c in name])
        except ValueError:
            raise AttributeError, name
            
    def __add__(self, other):
        assert isinstance(other, Vector3)
        return Vector3(self.x + other.x,
                       self.y + other.y,
                       self.z + other.z)
    
    def __sub__(self, other):
        assert isinstance(other, Vector3)
        return Vector3(self.x - other.x,
                       self.y - other.y,
                       self.z - other.z)
                       
    def __mul__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x * other.x,
                           self.y * other.y,
                           self.z * other.z)
        else:
            assert type(other) in (int, long, float)
            return Vector3(self.x * other, self.y * other, self.z * other)
    __rmul__ = __mul__
            
    def __div__(self, other):
        assert type(other) in (int, long, float)
        return Vector3(self.x / other, self.y / other, self.z / other)
        
    def __floordiv__(self, other):
        assert type(other) in (int, long, float)
        return Vector3(self.x // other, self.y // other, self.z // other)
            
    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)
        
    __pos__ = __copy__
    
    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        
    def lengthSquared(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2
        
    def normalize(self):
        m = self.length()
        if m != 0:
            self.x /= m
            self.y /= m
            self.z /= m
        return self
        
    def normalized(self):
        m = self.length()
        if m != 0:
            return Vector3(self.x / m, self.y / m, self.z / m)
        else:
            return self.copy()
            
    def dot(self, other):
        assert isinstance(other, Vector3)
        return self.x * other.x + self.y * other.y + self.z * other.z
        
    def cross(self, other):
        assert isinstance(other, Vector3)
        return Vector3(self.y * other.z - self.z * other.y,
                       self.z * other.x - self.x * other.z,
                       self.x * other.y - self.y * other.x)
        
    def angle(self, other):
        return Util.radianToDegree(self.angleInRadian(other))
            
    def angleInRadian(self, other):
        assert isinstance(other, Vector3)
        m2 = self.length() * other.length()
        if m2 == 0:
            return 0.0
        else:
            v = self.dot(other) / m2
            return math.acos( Util.clamp(v, -1.0, 1.0) )
            
    def project(self, other):
        assert isinstance(other, Vector3)
        n = other.normalized()
        return self.dot(n) * n
