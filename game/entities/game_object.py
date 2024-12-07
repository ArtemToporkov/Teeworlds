from game.enums import GameObjectData
from geometry.Vector import Vector
from game.constants import BACKGROUND_WIDTH, BACKGROUND_HEIGHT
from game.constants import GRAVITY
import os
from game.constants import WINDOW_HEIGHT, WINDOW_WIDTH
import pygame as pg


class SerializationMixin:
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


class ToolsMixin:
    def convert_coordinates(self, center):
        position = self.position - center + Vector(WINDOW_WIDTH, WINDOW_HEIGHT) / 2
        top_left = position - self.size / 2
        bottom_right = position + self.size / 2

        return position, top_left, bottom_right


class CollisionHandler:
    def __init__(self, game_object):
        self.game_object = game_object

    def collide(self, map):
        self.collide_x(map)
        self.collide_y(map)
        self.check_landed(map)

    def collide_x(self, map):
        self.game_object.move(Vector(self.game_object.velocity.x, 0))
        for corner in self.game_object.corners:
            key = self.get_block_key(corner, map.tile_size)
            block = map.blocks.get(key)
            if block is not None:
                self.game_object.move(-self.game_object.velocity.x, 0)
                self.correct_position_x(block)
                self.game_object.velocity.x = 0
                break
        else:
            self.game_object.move(-Vector(self.game_object.velocity.x, 0))

    def collide_y(self, map):
        self.game_object.move(Vector(0, self.game_object.velocity.y))
        for corner in self.game_object.corners:
            key = self.get_block_key(corner, map.tile_size)
            block = map.blocks.get(key)
            if block is not None:
                self.game_object.move(0, -self.game_object.velocity.y)
                self.correct_position_y(block)
                self.game_object.velocity.y = 0
                break
        else:
            self.game_object.move(Vector(0, -self.game_object.velocity.y))

    def check_landed(self, map):
        self.game_object.move(Vector(0, 2))
        self.game_object.is_landed = any(
            map.blocks.get(self.get_block_key(corner, map.tile_size)) is not None
            for corner in self.game_object.corners
        )
        self.game_object.move(Vector(0, -2))

    def correct_position_x(self, block):
        if self.game_object.velocity.x > 0:
            self.game_object.position.x = block.top_left.x - self.game_object.width / 2 - 1
        else:
            self.game_object.position.x = block.bottom_right.x + self.game_object.width / 2 + 1

    def correct_position_y(self, block):
        if self.game_object.velocity.y > 0:
            self.game_object.position.y = block.top_left.y - self.game_object.height / 2 - 1
        else:
            self.game_object.position.y = block.bottom_right.y + self.game_object.height / 2 + 1

    def get_block_key(self, corner, tile_size):
        return (
                corner // tile_size * tile_size
                + Vector(tile_size / 2, tile_size / 2)
        ).to_tuple


class ImageLoader:
    @staticmethod
    def load_image(sprite_path, object_width, object_height):
        image = None
        if sprite_path is not None:
            image = pg.image.load(sprite_path)
            image = pg.transform.scale(image, (object_width, object_height))

        return image


class GameObject(SerializationMixin, ToolsMixin):
    def __init__(self, x, y, width=0, height=0, sprite_path: os.path = None):
        self.position = Vector(x, y)
        self.width = width
        self.height = height
        self.size = Vector(width, height)
        self.velocity = Vector(0, 0)
        self.hitbox_color = (255, 0, 0)

        self.sprite_path = sprite_path
        self.image = ImageLoader.load_image(sprite_path, width, height)
        self.frames = 0

        self.alive = True

        self.top_right = Vector(self.position.x + self.width, self.position.y + self.height)
        self.bottom_right = Vector(self.position.x + self.width, self.position.y - self.height)
        self.bottom_left = Vector(self.position.x - self.width, self.position.y - self.height)
        self.top_left = Vector(self.position.x - self.width, self.position.y + self.height)
        self.corners = [self.top_right, self.bottom_right, self.bottom_left, self.top_left]

        self.direction = Vector(0, 1)
        self.collision_handler = CollisionHandler(self)
        self.is_landed = False

    def intersects(self, other) -> bool:
        result = True
        if self.position.x > other.position.x + other.width or self.position.x + self.width < other.position.x:
            result = False
        if self.position.y > other.position.y + other.height or self.position.y + self.height < other.position.y:
            result = False
        self.hitbox_color = (255, 0, 0) if not result else (0, 255, 0)
        return result

    def move(self, move_vector: Vector) -> None:
        self.position += move_vector

    def get_coordinates_offset_by_center(self, center: Vector) -> Vector:
        position = self.position - center + Vector(WINDOW_WIDTH, WINDOW_HEIGHT) / 2
        return position

    def update(self):
        if self.velocity.length() > 25:
            self.velocity = self.velocity.normalize() * 25
        self.position += self.velocity
        self.apply_forces()
        # self.animate()

    def apply_forces(self):
        if not self.is_landed:
            self.velocity = self.velocity + GRAVITY

    def collide(self, map):
        self.collision_handler.collide(map)

    def draw(self, screen, center):
        if self.image is None:
            position, top_left, bottom_right = self.convert_coordinates(center)
            pg.draw.rect(
                screen, (255, 255, 0), (top_left.x, top_left.y, self.width, self.height)
            )
            return

        pos, top_left, _ = self.convert_coordinates(center)
        rect = top_left.tuple + self.size.to_tuple
        if self.sprite_path is not None:
            screen.blit(self.image, rect)

    def draw_hitbox(self, screen):
        # Рисование хитбокса <лишнее.>
        pg.draw.rect(screen, self.hitbox_color, (self.position.x, self.position.y, self.width, self.height), 2)

    def get_particle(self):
        return None
