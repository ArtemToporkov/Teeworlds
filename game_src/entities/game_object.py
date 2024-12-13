from game_src.utils.enums import GameObjectData, Collisions, TypeData
from geometry.vector import Vector
import os
from game_src.constants import WINDOW_HEIGHT, WINDOW_WIDTH, ASSETS_PATH
import pygame as pg


class SerializationMixin:
    def to_dict(self):
        from game_src.utils.serialization_tools import packing_path
        return {
            TypeData.TYPE.value: type(self).__name__,
            GameObjectData.ID.value: self.id,
            GameObjectData.POSITION_X.value: self.position.x,
            GameObjectData.POSITION_Y.value: self.position.y,
            GameObjectData.VELOCITY.value: self.velocity.to_tuple(),
            GameObjectData.WIDTH.value: self.width,
            GameObjectData.HEIGHT.value: self.height,
            GameObjectData.DIRECTION.value: self.look_direction.to_tuple(),
            GameObjectData.SPRITE_PATH.value: packing_path(self.sprite_path),
        }

    @staticmethod
    def from_dict(data):
        from game_src.utils.serialization_tools import unpacking_path
        game_obj = GameObject(
            x=data[GameObjectData.POSITION_X.value],
            y=data[GameObjectData.POSITION_Y.value],
            width=data[GameObjectData.WIDTH.value],
            height=data[GameObjectData.HEIGHT.value],
            sprite_path=unpacking_path(data[GameObjectData.SPRITE_PATH.value]),
        )
        game_obj.velocity = Vector(*data[GameObjectData.VELOCITY.value])
        game_obj.look_direction = Vector(*data[GameObjectData.DIRECTION.value])
        return game_obj


class ImageLoader:
    @staticmethod
    def load_image(sprite_path, object_width, object_height):
        image = None
        if sprite_path is not None:
            image = pg.image.load(sprite_path)
            image = pg.transform.scale(image, (object_width, object_height))

        return image


class GameObject(SerializationMixin):
    def __init__(self, x, y, width=0, height=0, sprite_path: os.path = None):
        self.position = Vector(x, y)
        self.size = Vector(width, height)
        self.velocity = Vector(0, 0)
        self.hitbox_color = (255, 0, 0)
        self.width = width
        self.height = height
        # TODO: убрать width и height, так как они почти всегда равны размеру изображения

        self.sprite_path = sprite_path
        self.image = ImageLoader.load_image(sprite_path, width, height)
        self.frames = 0

        self.alive = True
        self.id = None

        self.top_left = self.position
        self.top_right = self.position + Vector(self.width, 0)
        self.bottom_left = self.position + Vector(0, self.height)
        self.bottom_right = self.position + Vector(self.width, self.height)
        self.corners = [self.top_right, self.top_right, self.bottom_left, self.bottom_left]

        self.look_direction = Vector(0, 1)
        self.is_landed = False

    def intersects(self, other: 'GameObject') -> bool:
        result = True
        if self.position.x > other.position.x + other.width or self.position.x + self.width < other.position.x:
            result = False
        if self.position.y > other.position.y + other.height or self.position.y + self.height < other.position.y:
            result = False
        self.hitbox_color = (255, 0, 0) if not result else (0, 255, 0)
        return result

    def predict_collisions(self, platforms: list['Platform'], potential_move: Vector) -> dict[Collisions, bool]:
        current_collisions = {
            col: False for col in [Collisions.X_RIGHT, Collisions.X_LEFT, Collisions.Y_UP, Collisions.Y_DOWN]
        }
        for platform in platforms:
            collisions = platform.get_collisions(self, potential_move)
            for key in collisions.keys():
                current_collisions[key] = collisions[key] or current_collisions[key]
        return current_collisions

    def move(self, move_vector: Vector) -> None:
        self.position += move_vector
        self.top_right += move_vector
        self.top_left += move_vector
        self.bottom_left += move_vector
        self.bottom_right += move_vector

    def get_coordinates_offset_by_center(self, center: 'GameObject') -> Vector:
        position = self.position - center.position + Vector(WINDOW_WIDTH, WINDOW_HEIGHT) / 2
        position -= Vector(center.width / 2, center.height / 2)
        return position

    def get_coordinates_offset_by_self(self, vector: Vector) -> Vector:
        position = vector - self.position + Vector(WINDOW_WIDTH, WINDOW_HEIGHT) / 2
        position -= Vector(self.width / 2, self.height / 2)
        return position

    def update(self):
        if self.velocity.length() > 25:
            self.velocity = self.velocity.normalize() * 25
        self.position += self.velocity

    def draw(self, screen, center):
        new_coordinates = self.get_coordinates_offset_by_center(center)
        screen.blit(self.image, (new_coordinates.x, new_coordinates.y, self.width, self.height))

    def draw_hitbox(self, screen, center):
        new_coordinates = self.get_coordinates_offset_by_center(center)
        pg.draw.circle(screen, self.hitbox_color, (new_coordinates.x + self.width / 2, new_coordinates.y + self.height / 2), 2)
        pg.draw.rect(screen, self.hitbox_color, (new_coordinates.x, new_coordinates.y, self.width, self.height), 2)

    def interact(self, other: 'GameObject'):
        pass

    def get_particle(self):
        return None
