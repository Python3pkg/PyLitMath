import math
import Util

class Vector2(object):
    __slots__ = ['x', 'y']
    __hash__ = None

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
        
    def set(self, x, y):
        self.x = x
        self.y = y
        return self
        
    def __copy__(self):
        return self.__class__(self.x, self.y)
    copy = __copy__
    
    def __repr__(self):
        return 'Vector2(%.2f, %.2f)' % (self.x, self.y)
        
    def __eq__(self, other):
        if isinstance(other, Vector2):
            return Util.isEqual(self.x, other.x) and \
                   Util.isEqual(self.y, other.y)
        else:
            return False
        
    def __ne__(self, other):
        return not self.__eq__(other)
        
    def __nonzero__(self):
        return self.x != 0 or self.y != 0
               
    def isZero(self):
        return self.x == 0 and self.y == 0
        
    def __len__(self):
        return 2
        
    def __getitem__(self, key):
        assert type(key) in (int, long)
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == -1:
            return self.y
        elif key == -2:
            return self.x
        else:
            raise IndexError, "Vector2 index out of range"
        
    def __setitem__(self, key, value):
        assert type(key) in (int, long)
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == -1:
            self.y = value
        elif key == -2:
            self.x = value
        else:
            raise IndexError, "Vector2 index out of range"
        
    def __iter__(self):
        return iter((self.x, self.y))
        
    def __getattr__(self, name):
        try:
            return tuple([(self.x, self.y)['xy'.index(c)] \
                          for c in name])
        except ValueError:
            raise AttributeError, name

    def __add__(self, other):
        assert isinstance(other, Vector2)
        return Vector2(self.x + other.x,
                       self.y + other.y)
    
    def __sub__(self, other):
        assert isinstance(other, Vector2)
        return Vector2(self.x - other.x,
                       self.y - other.y)
                           
    def __mul__(self, other):
        assert type(other) in (int, long, float)
        return Vector2(self.x * other, self.y * other)
    __rmul__ = __mul__
    
    def __div__(self, other):
        assert type(other) in (int, long, float)
        return Vector2(self.x / other, self.y / other)
        
    def __floordiv__(self, other):
        assert type(other) in (int, long, float)
        return Vector2(self. x // other, self.y // other)
        
    def __neg__(self):
        return Vector2(-self.x, -self.y)
        
    __pos__ = __copy__
    
    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
        
    def lengthSquared(self):
        return self.x ** 2 + self.y ** 2
        
    def normalize(self):
        d = self.length()
        if d != 0:
            self.x /= d
            self.y /= d
        return self
        
    def normalized(self):
        d = self.length()
        if d != 0:
            return Vector2(self.x / d, self.y / d)
        else:
            return self.copy()
            
    def dot(self, other):
        assert isinstance(other, Vector2)
        return self.x * other.x + self.y * other.y
        
    def angle(self, other):
        return Util.radianToDegree(self.angleInRadian(other))
    
    def angleInRadian(self, other):
        assert isinstance(other, Vector2)
        m2 = self.length() * other.length()
        if m2 == 0:
            return 0.0
        else:
            v = self.dot(other) / m2
            return math.acos( Util.clamp(v, -1.0, 1.0) )
            
    def project(self, other):
        assert isinstance(other, Vector2)
        n = other.normalized()
        return self.dot(n) * n