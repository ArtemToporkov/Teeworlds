from geometry.Vector import Vector
import pygame as pg
from game.constants import BACKGROUND_WIDTH, BACKGROUND_HEIGHT


class GameObject:
    def __init__(self, x, y, width=0, height=0):
        self.position = Vector(x, y)
        self.size = Vector(width, height)
        self.width = width
        self.height = height

    @property
    def top_left(self):
        return self.position - self.size / 2

    @property
    def bottom_right(self):
        return self.position + self.size / 2

    @property
    def corners(self):
        return [
            Vector(self.top_left.x, self.top_left.y),
            Vector(self.top_left.x, self.bottom_right.y),
            Vector(self.bottom_right.x, self.bottom_right.y),
            Vector(self.bottom_right.x, self.top_left.y),
        ]

    def intersects(self, other) -> bool:
        return max(self.top_left.x, other.top_left.x) <= min(
            self.bottom_right.x, other.bottom_right.x
        ) and max(self.top_left.y, other.top_left.y) <= min(
            self.bottom_right.y, other.bottom_right.y
        )

    def draw(self, screen, center):
        position, top_left, bottom_right = self.convert_coordinates(center)
        pg.draw.rect(
            screen, (255, 255, 0), (top_left.x, top_left.y, self.width, self.height)
        )

    def convert_coordinates(self, center):
        position = self.position - center + Vector(BACKGROUND_WIDTH, BACKGROUND_HEIGHT) / 2
        top_left = position - self.size / 2
        bottom_right = position + self.size / 2

        return position, top_left, bottom_right

    def get_particle(self):
        return None

    def to_dict(self):
        return {
            "x": self.position.x,
            "y": self.position.y,
            "width": self.width,
            "height": self.height,
        }

    @staticmethod
    def from_dict(data):
        return GameObject(
            x=data["x"],
            y=data["y"],
            width=data.get("width", 0),
            height=data.get("height", 0),
        )
