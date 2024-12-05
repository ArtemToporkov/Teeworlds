from geometry.Vector import Vector
import os


class Entity:
    def __init__(self, x, y, width=0, height=0, sprite_path: os.path = None):
        self.position = Vector(x, y)
        self.width = width
        self.height = height
        self.sprite_path = sprite_path
        self.top_right = Vector(self.position + self.width, self.position + self.height)
        self.bottom_right = Vector(self.position + self.width, self.position - self.height)
        self.bottom_left = Vector(self.position - self.width, self.position - self.height)
        self.top_left = Vector(self.position - self.width, self.position + self.height)

    def intersects(self, other) -> bool:
        return (max(self.top_left.x, other.top_left.x) <= min(self.bottom_right.x, other.bottom_right.x)
                and max(self.top_left.y, other.top_left.y) <= min(self.bottom_right.y, other.bottom_right.y))




