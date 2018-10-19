import math


# This class should provide you with all the basic vector operations that you need
# The vectors found in the GameTickPacket will be flatbuffer vectors. Cast them to Vec3 like this:
# car_location = Vec3().set(car.physics.location)
# Remember that the in-game axis are left-handed.
# When in doubt visit: https://github.com/RLBot/RLBot/wiki/Useful-Game-Values
class Vec3:
    def __init__(self, x: float=0, y: float=0, z: float=0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __mul__(self, scale):
        return Vec3(self.x * scale, self.y * scale, self.z * scale)

    def __rmul__(self, scale):
        return self * scale

    def __truediv__(self, scale):
        scale = 1 / float(scale)
        return self * scale

    def __str__(self):
        return "Vec3(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"

    def flat(self):
        """Returns a new Vec3 that equals this Vec3 but projected onto the ground plane."""
        return Vec3(self.x, self.y, 0)

    def length(self):
        """Returns the length of the vector."""
        return self.magnitude()

    def magnitude(self):
        """Returns the magnitude of the vector."""
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def dist(self, other):
        """Returns the distance between this vector and another vector using pythagoras."""
        return (self - other).length()

    def normalized(self):
        """Returns a vector with the same direction but a magnitude/length of one."""
        return self / self.length()

    def rescale(self, new_len):
        """Returns a vector with the same direction but a different length."""
        return new_len * self.normalized()

    def mul_components(self, other):
        """Multiply the components of each vector to create a new vector.
        a.mul_components(b) = Vec3(a.x*b.x, a.y*b.y, a.z*b.z)."""
        return Vec3(self.x*other.x, self.y*other.y, self.z*other.z)

    def rotate_2d(self, ang):
        """Returns a new vector, that has been rotated around the z-axis."""
        c = math.cos(ang)
        s = math.sin(ang)
        return Vec3(c * self.x - s * self.y,
                    s * self.x + c * self.y)

    def lerp(self, other, t):
        """Use linear interpolation to find a vector between two vectors. When t=0, you get the original vector. When
        t=1, you get the other vector. When t is between 0 and 1 you get a vector in between. t can also be greater
        than 1 or less than 0."""
        return self * (1 - t) + other * t

    def dot(self, other):
        """Returns the dot product."""
        return self.x*other.x + self.y*other.y + self.z*other.z

    def cross(self, other):
        """Returns the cross product."""
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def ang_2d(self):
        """Returns the angle this vector and Vec3(1, 0) in the xy-plane. Angle will be between -pi and +pi."""
        return math.atan2(self.y, self.x)

    def ang_to(self, ideal):
        """Returns the angle to the ideal vector. Angle will be between 0 and pi."""
        cos_ang = self.dot(ideal) / (self.length() * ideal.length())
        return math.acos(cos_ang)

    def ang_to_2d(self, ideal):
        """Returns the angle to the ideal vector in the xy-plane. Angle will be between -pi and +pi."""
        current_in_radians = math.atan2(self.y, self.x)
        ideal_in_radians = math.atan2(ideal.y, ideal.x)

        diff = ideal_in_radians - current_in_radians

        # make sure that diff is between -pi and +pi.
        if abs(diff) > math.pi:
            if diff < 0:
                diff += 2 * math.pi
            else:
                diff -= 2 * math.pi

        return diff

    def proj_onto(self, other):
        """Returns the projection of this vector onto another vector. The projection is a vector that is parallel
        with the other vector."""
        try:
            return (self.dot(other) / other.dot(other)) * other
        except ZeroDivisionError:
            return Vec3()

    def proj_onto_size(self, other):
        """Returns the size of the projection of this vector onto another vector. Can return negative numbers!
        Useful when you just want to know \"how much of this vector points in that direction.\""""
        try:
            other = other.normalized()
            return self.dot(other) / other.dot(other)   # can be negative!
        except ZeroDivisionError:
            return self.length()

    def set(self, some):
        """Sets this vector to a copy of another vector. Even works for flatbuffer vectors."""
        self.x = some.x
        self.y = some.y
        self.z = some.z
        return self

    def tuple(self):
        """Returns this vector as a tuple (x, y, z)"""
        return self.x, self.y, self.z

    def copy(self):
        """Returns a copy of this vector."""
        return Vec3(self.x, self.y, self.z)


X = Vec3(x=1)
Y = Vec3(y=1)
Z = Vec3(z=1)
