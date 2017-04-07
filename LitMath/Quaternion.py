import math
import Util

class Quaternion(object):
    __slots__ = ['x', 'y', 'z', 'w']
    __hash__ = None
    
    def __init__(self, x=0.0, y=0.0, z=0.0, w=1.0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        
    def set(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        return self
        
    def __copy__(self):
        return Quaternion(self.x, self.y, self.z, self.w)
    copy = __copy__
    
    def __repr__(self):
        return 'Quaternion(%.2f, %.2f, %.2f, %.2f)' % \
               (self.x, self.y, self.z, self.w)
            
    def magnitude(self):
        return math.sqrt(self.x ** 2 +
                         self.y ** 2 +
                         self.z ** 2 +
                         self.w ** 2)
            
    def normalize(self):
        len = self.magnitude()
        if len != 0:
            self.x /= len
            self.y /= len
            self.z /= len
            self.w /= len   
        return self
        
    def normalized(self):
        len = self.magnitude()
        if len == 0:
            return self.copy()
        else:
            return Quaternion(self.x / len, self.y / len, self.z / len, self.w / len)
            
    def invert(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z
        return self
        
    def inverse(self):
        return Quaternion(-self.x, -self.y, -self.z, self.w)
               
    def __mul__(self, other):
        '''Multiplies two quaternions.'''
        assert isinstance(other, Quaternion)
        return Quaternion(
            self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
            self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x,
            self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w,
            self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z)
            
    def multiplyPoint(self, pnt):
        '''Rotates the point pnt by this quaternion.'''
        import Vector3
        assert isinstance(other, Vector3)
        
        x = self.x
        y = self.y
        z = self.z
        w = self.w
        x2 = self.x * self.x
        y2 = self.y * self.y
        z2 = self.z * self.z
        w2 = self.w * self.w
        
        dx = (x2+w2-y2-z2)*other.x + 2.0*(x*y-z*w)*other.y + 2.0*(x*z+y*w)*other.z
        dy = 2.0*(x*y+z*w)*other.x + (w2-x2+y2-z2)*other.y + 2.0*(y*z-x*w)*other.z
        dz = 2.0*(x*z-y*w)*other.x + 2.0*(x*w+y*z)*other.y + (w2-x2-y2+z2)*other.z
        
        return Vector3(dx, dy, dz)
        
    def toMatrix4(self):
        '''Converts a rotation to 4x4 matrix.'''
        # reference:FreeCAD Rotation.cpp
        x = self.x
        y = self.y
        z = self.z
        w = self.w
        
        import Matrix4
        matrix = Matrix4()
        matrix.m11 = 1.0-2.0*(y*y+z*z)
        matrix.m12 = 2.0*(x*y-z*w)
        matrix.m13 = 2.0*(x*z+y*w)
        matrix.m14 = 0.0
    
        matrix.m21 = 2.0*(x*y+z*w)
        matrix.m22 = 1.0-2.0*(x*x+z*z)
        matrix.m23 = 2.0*(y*z-x*w)
        matrix.m24 = 0.0
    
        matrix.m31 = 2.0*(x*z-y*w)
        matrix.m32 = 2.0*(y*z+x*w)
        matrix.m33 = 1.0-2.0*(x*x+y*y)
        matrix.m34 = 0.0
    
        matrix.m41 = 0.0
        matrix.m42 = 0.0
        matrix.m43 = 0.0
        matrix.m44 = 1.0
        
        return matrix
        
    def toAxisAngle(self):
        '''Converts a rotation to axis-angle representation(angle in degree).'''
        axis, angle = self.toAxisAngleInRadian()
        return axis, Util.radianToDegree(angle)
        
    def toAxisAngleInRadian(self):
        '''Converts a rotation to axis-angle representation(angle in radian).'''
        import Vector3
        # reference:FreeCAD Rotation.cpp
        if self.w > -1.0 and self.w < 1.0:
            t = math.acos(self.w)
            scale = math.sin(t)
            if Util.isEqualZero(scale):
                return Vector3(0,0,1), 0.0
            else:
                axis = Vector3(self.x / scale, self.y / scale, self.z / scale)
                return axis, 2*t
        else:
            return Vector3(0,0,1), 0.0
            
    def toEulerXYZ(self):
        def clamp(x):
            return min( max( x, -1 ), 1 )
            
        sqx = self.x * self.x
        sqy = self.y * self.y
        sqz = self.z * self.z
        sqw = self.w * self.w
        
        import Vector3
        euler = Vector3.Vector3()
        euler.x = math.atan2( 2 * ( self.x * self.w - self.y * self.z ), ( sqw - sqx - sqy + sqz ) )
        euler.y = math.asin(  clamp( 2 * ( self.x * self.z + self.y * self.w ) ) )
        euler.z = math.atan2( 2 * ( self.z * self.w - self.x * self.y ), ( sqw + sqx - sqy - sqz ) )
        return euler
        
    def toEulerZXY(self):
        def clamp(x):
            return min( max( x, -1 ), 1 )
            
        sqx = self.x * self.x
        sqy = self.y * self.y
        sqz = self.z * self.z
        sqw = self.w * self.w
        
        import Vector3
        euler = Vector3.Vector3()
        euler.x = math.asin(  clamp( 2 * ( self.x * self.w + self.y * self.z ) ) )
        euler.y = math.atan2( 2 * ( self.y * self.w - self.z * self.x ), ( sqw - sqx - sqy + sqz ) )
        euler.z = math.atan2( 2 * ( self.z * self.w - self.x * self.y ), ( sqw - sqx + sqy - sqz ) )
        return euler
        
    def setIdentity(self):
        self.set(0.0, 0.0, 0.0, 1.0)
        return self
        
    @staticmethod
    def Identity():
        '''Returns the identity quaternion.'''
        return Quaternion(0.0, 0.0, 0.0, 1.0)
        
    @staticmethod
    def Matrix4(matrix):
        import Matrix4
        assert isinstance(matrix, Matrix4)

        quat = Quaternion()
        M = matrix
        trace = M.m11 + M.m22 + M.m33

        if trace > 0:
            s = 0.5 / math.sqrt(trace + 1.0)
            quat.w = 0.25 / s
            quat.x = (M.m32 - M.m23 ) * s
            quat.y = (M.m13 - M.m31 ) * s
            quat.z = (M.m21 - M.m12 ) * s
        elif M.m11 > M.m22 and M.m11 > M.m33:
            s = 2.0 * math.sqrt(1.0 + M.m11 - M.m22 - M.m33)
            quat.w = (M.m32 - M.m23) / s
            quat.x = 0.25 * s
            quat.y = (M.m12 + M.m21) / s
            quat.z = (M.m13 + M.m31) / s
        elif M.m22 > M.m33:
            s = 2.0 * math.sqrt(1.0 + M.m22 - M.m11 - M.m33)
            quat.w = (M.m13 - M.m31) / s
            quat.x = (M.m12 + M.m21) / s
            quat.y = 0.25 * s;
            quat.z = (M.m23 + M.m32) / s
        else:
            s = 2.0 * math.sqrt(1.0 + M.m33 - M.m11 - M.m22)
            quat.w = (M.m21 - M.m12) / s
            quat.x = (M.m13 + M.m31) / s
            quat.y = (M.m23 + M.m32) / s
            quat.z = 0.25 * s
            
        return quat
        
    @staticmethod
    def AxisAngle(axis, angle):
        '''Creates a rotation which rotates angle degrees around axis.'''
        import Vector3
        assert isinstance(axis, Vector3) and \
               type(angle) in (int, long, float)
        
        return Quaternion.AxisAngleInRadian(axis, Util.degreeToRadian(angle))
        
    @staticmethod
    def AxisAngleInRadian(axis, angle):
        '''Creates a rotation which rotates angle degrees around axis.'''
        import Vector3
        assert isinstance(axis, Vector3) and \
               type(angle) in (int, long, float)
        
        axis = axis.normalized()
        scale = math.sin(angle / 2)
        
        quat = Quaternion()
        quat.w = math.cos(angle / 2)
        quat.x = axis.x * scale
        quat.y = axis.y * scale
        quat.z = axis.z * scale
        
        return quat
        
    @staticmethod
    def FromToRotation(f, to):
        '''Creates a rotation which rotates from from(Vector) to to(Vector).'''
        import Vector3
        assert isinstance(f, Vector3) and isinstance(to, Vector3)
        
        # reference:FreeCAD Rotation.cpp
        u = f.normalized()
        v = to.normalized()
        dot = u.dot(v)
        w = u.cross(v)
        
        # parallel vectors
        if w.magnitude() == 0:
            # same direction
            if dot >= 0:
                return Quaternion(0.0, 0.0, 0.0, 1.0)
            else:
                t = u.cross(Vector3(1.0, 0.0, 0.0))
                if Util.isEqualZero(t.magnitude()):
                    t = u.cross(Vector3(0.0, 1.0, 0.0))
                return Quaternion(t.x, t.y, t.z, 0.0)
        else:
            angleInRad = math.acos(dot)
            return Quaternion.AxisAngleInRadian(w, angleInRad)
            
    @staticmethod
    def EulerXYZ(x, y, z):
        x = Util.degreeToRadian(x)
        y = Util.degreeToRadian(y)
        z = Util.degreeToRadian(z)
        
        c1 = math.cos(x / 2)
        c2 = math.cos(y / 2)
        c3 = math.cos(z / 2)
        s1 = math.sin(x / 2)
        s2 = math.sin(y / 2)
        s3 = math.sin(z / 2)
        
        quat = Quaternion()
        quat.x = s1 * c2 * c3 + c1 * s2 * s3
        quat.y = c1 * s2 * c3 - s1 * c2 * s3
        quat.z = c1 * c2 * s3 + s1 * s2 * c3
        quat.w = c1 * c2 * c3 - s1 * s2 * s3
        return quat
        
    @staticmethod
    def EulerZXY(x, y, z):
        x = Util.degreeToRadian(x)
        y = Util.degreeToRadian(y)
        z = Util.degreeToRadian(z)
        
        c1 = math.cos(x / 2)
        c2 = math.cos(y / 2)
        c3 = math.cos(z / 2)
        s1 = math.sin(x / 2)
        s2 = math.sin(y / 2)
        s3 = math.sin(z / 2)
        
        quat = Quaternion()
        quat.x = s1 * c2 * c3 - c1 * s2 * s3
        quat.y = c1 * s2 * c3 + s1 * c2 * s3
        quat.z = c1 * c2 * s3 + s1 * s2 * c3
        quat.w = c1 * c2 * c3 - s1 * s2 * s3
        return quat