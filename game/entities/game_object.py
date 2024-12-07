import pygame

from game.enums import GameObjectData
from geometry.Vector import Vector
import os
from game.constants import WINDOW_HEIGHT, WINDOW_WIDTH


class GameObject:
    def __init__(self, x, y, width=0, height=0, sprite_path: os.path = None):
        self.position = Vector(x, y)
        self.width = width
        self.height = height
        self.sprite_path = sprite_path
        self.hitbox_color = (255, 0, 0)

    def intersects(self, other) -> bool:
        result = True
        if self.position.x > other.position.x + other.width or self.position.x + self.width < other.position.x:
            result = False
        if self.position.y > other.position.y + other.height or self.position.y + self.height < other.position.y:
            result = False
        self.hitbox_color = (255, 0, 0) if not result else (0, 255, 0)
        return result

    def get_coordinates_offset_by_center(self, center: Vector) -> Vector:
        position = self.position - center + Vector(WINDOW_WIDTH, WINDOW_HEIGHT) / 2
        return position

    def to_dict(self):
        return {
            GameObjectData.X: self.position.x,
            GameObjectData.Y: self.position.y,
            GameObjectData.WIDTH: self.width,
            GameObjectData.HEIGHT: self.height,
            GameObjectData.SPRITE_PATH: self.sprite_path
        }
    
    def draw_hitbox(self, screen):
        # Рисование хитбокса
        pygame.draw.rect(screen, self.hitbox_color, (self.position.x, self.position.y, self.width, self.height), 2)

    @staticmethod
    def from_dict(data):
        return GameObject(
            x=data[GameObjectData.X],
            y=data[GameObjectData.Y],
            width=data.get(GameObjectData.WIDTH, 0),
            height=data.get(GameObjectData.HEIGHT, 0),
            sprite_path=data[GameObjectData.SPRITE_PATH]
        )




