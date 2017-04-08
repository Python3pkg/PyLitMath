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
        
    def copy(self):
        import copy
        return copy.copy(self)
    
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
        
    def __neg__(self):
        return Vector2(-self.x, -self.y)
    
    @property
    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    @property
    def lengthSquared(self):
        return self.x ** 2 + self.y ** 2
        
    def normalize(self):
        d = self.length
        if d != 0:
            self.x /= d
            self.y /= d
        return self
    
    @property
    def normalized(self):
        d = self.length
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
        m2 = self.length * other.length
        if m2 == 0:
            return 0.0
        else:
            v = self.dot(other) / m2
            return math.acos( Util.clamp(v, -1.0, 1.0) )