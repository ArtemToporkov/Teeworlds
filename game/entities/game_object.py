from game.enums import GameObjectData
from geometry.Vector import Vector
import os


class GameObject:
    def __init__(self, x, y, width=0, height=0, sprite_path: os.path = None):
        self.position = Vector(x, y)
        self.width = width
        self.height = height
        self.sprite_path = sprite_path
        self.top_right = Vector(self.position.x + self.width, self.position.y + self.height)
        self.bottom_right = Vector(self.position.x + self.width, self.position.y - self.height)
        self.bottom_left = Vector(self.position.x - self.width, self.position.y - self.height)
        self.top_left = Vector(self.position.x - self.width, self.position.y + self.height)

    def intersects(self, other) -> bool:
        return (max(self.top_left.x, other.top_left.x) <= min(self.bottom_right.x, other.bottom_right.x)
                and max(self.top_left.y, other.top_left.y) <= min(self.bottom_right.y, other.bottom_right.y))

    def move(self, move_vector: Vector) -> None:
        self.position += move_vector

    def to_dict(self):
        return {
            GameObjectData.X: self.position.x,
            GameObjectData.Y: self.position.y,
            GameObjectData.WIDTH: self.width,
            GameObjectData.HEIGHT: self.height,
            GameObjectData.SPRITE_PATH: self.sprite_path
        }

    @staticmethod
    def from_dict(data):
        return GameObject(
            x=data[GameObjectData.X],
            y=data[GameObjectData.Y],
            width=data.get(GameObjectData.WIDTH, 0),
            height=data.get(GameObjectData.HEIGHT, 0),
            sprite_path=data[GameObjectData.SPRITE_PATH]
        )




