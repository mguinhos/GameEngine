from dataclasses import dataclass
from math import sqrt

@dataclass
class Vector:
    x: float
    y: float
    z: float=0.0

    def __abs__(self):
        return type(self)(abs(self.x), abs(self.y), abs(self.z))

    def __add__(self, value: "Vector"):
        return type(self)(self.x + value.x, self.y + value.y, self.z + value.z)
    
    def __sub__(self, value: "Vector"):
        return type(self)(self.x - value.x, self.y - value.y, self.z - value.z)
    
    def __mul__(self, value: "Vector"):
        return type(self)(self.x * value.x, self.y * value.y, self.z * value.z)
    
    def __div__(self, value: "Vector"):
        return type(self)(self.x / value.x, self.y / value.y, self.z / value.z)
    
    def copy(self):
        return type(self)(self.x, self.y, self.z)
    
    def cross(self, vector: "Vector"):
        return type(self)(
            self.y * vector.z - self.z - vector.y,
            self.z * vector.x - self.x - vector.z,
            self.x * vector.y - self.y - vector.x
        )

    
    @property
    def flat(self):
        return [self.x, self.y, self.z]
    
    @property
    def magnitude(self):
        return sqrt(self.x** 2 + self.y**2 + self.z**2)

        

    @property
    def normalized(self):
        magnitude = self.magnitude

        if magnitude > 0.00001:
            return type(self)(self.x / magnitude, self.y / magnitude, self.z / magnitude)

        return type(self)(0, 0, 0)

class Position(Vector):
    pass

class Rotation(Vector):
    pass

class Size(Vector):
    pass