import math
from dataclasses import dataclass


@dataclass
class Vector:
    x: float
    y: float

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, coefficient):
        return Vector(self.x * coefficient, self.y * coefficient)

    def __rmul__(self, coefficient):
        return Vector(self.x * coefficient, self.y * coefficient)

    def __truediv__(self, coefficient):
        return Vector(self.x / coefficient, self.y / coefficient)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"(x: {self.x}, y: {self.y})"

    def normalize(self):
        length = self.length()
        return self / length if length != 0 else Vector(0, 0)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def rotate(self, angle):
        sin = math.sin(angle)
        cos = math.cos(angle)
        x = self.x * cos - self.y * sin
        y = self.x * sin + self.y * cos
        return Vector(x, y)

    def to_tuple(self):
        return self.x, self.y
