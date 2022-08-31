from cmath import acos, asin, atan
from locale import normalize
from math import sin, cos, atan2, degrees, radians

from .mesh import Position, Rotation

class Camera:
    def __init__(self, position=Position(0, 0, 0), rotation=Rotation(0, 0, 0)):
        self.position = position.copy()
        self.rotation = rotation.copy()
    
    def advance(self, by: float):
        sin_rx, cos_rx = sin(radians(self.rx)), cos(radians(self.rx))
        sin_ry, cos_ry = sin(radians(self.ry)), cos(radians(self.ry))

        self.position += Position(
            by * -sin_ry,
            by * sin_rx,
            by * cos_ry
        )

        return self
    
    def look(self, position: Position, up=Position(0, 1, 0)):
        delta = (self.position - position).normalized

        self.rotation.x = 0 + degrees(atan2(delta.y, delta.z))
        self.rotation.y = 0 - degrees(atan2(delta.x, delta.z))
        
        return self