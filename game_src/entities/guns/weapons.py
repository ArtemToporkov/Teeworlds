import os

from game_src.entities.guns.bullets import BulletData, Grenade, BlowingBulletData, Bullet, BlowingBullet
from game_src.entities.game_object import GameObject
from geometry.vector import Vector
from game_src.constants import ASSETS_PATH
import pygame as pg
import math
import random


BULLETS_PATH = os.path.join(ASSETS_PATH, "weapons", "bullets")


class ImageLoader:
    @staticmethod
    def load_sprite(sprite_path, width):
        sprite = None
        if sprite_path:
            sprite = pg.image.load(sprite_path)
            h = width * sprite.get_height() / sprite.get_width()
            sprite = pg.transform.scale(pg.image.load(sprite_path), (width, h))
        return sprite


class Weapon(GameObject):
    def __init__(self, x, y, width, height, sprite_path):
        super().__init__(x, y, width=width, height=height, sprite_path=sprite_path)
        self.image = ImageLoader.load_sprite(sprite_path, width)
        self.kickback = 0
        self.direction = Vector(0, 0)
        self.dist = 30
        pass

    def get_bullets(self):
        pass

    def draw(self, screen, center):
        angle = -math.atan2(self.direction.y, self.direction.x) / math.pi * 180
        new_coordinates = self.get_coordinates_offset_by_center(center)
        rect = self.image.get_rect(center=(new_coordinates.x + center.width / 2, new_coordinates.y + center.height / 2))
        image = self.image
        if angle > 90 or angle < -90:
            image = pg.transform.flip(image, False, True)
        image = pg.transform.rotate(image, angle)

        screen.blit(image, rect)


class Pistol(Weapon):
    def get_bullets(self):
        bullet_pos = self.position
        bullet = Bullet(
            bullet_pos.x,
            bullet_pos.y,
            30,
            30,
            100,
            sprite_path=os.path.join(BULLETS_PATH, "bullet.png"),
        )
        bullet.velocity = self.direction * 50
        return [bullet]


class ShotGun(Weapon):
    def get_bullets(self):
        bullets = []
        for i in range(5):
            bullet_pos = (
                self.position
                + self.direction * self.dist / 2
                + Vector((random.random() - 0.5) * 10, (random.random() - 0.5) * 10)
            )
            bullet = Bullet(
                bullet_pos.x,
                bullet_pos.y,
                20,
                20,
                60,
                sprite_path=os.path.join(BULLETS_PATH, "bullet.png"),
            )
            bullet.velocity = self.direction.rotate(random.random() - 0.5) * 50
            bullets.append(bullet)

        return bullets


class Rocket(Weapon):
    def __init__(self, x, y, width, height, sprite_path):
        super().__init__(x, y, width, height, sprite_path)
        self.kickback = 20

    def get_bullets(self):
        bullets = []
        bullet_pos = self.position + self.direction * self.dist / 2
        bullet = BlowingBullet(
            bullet_pos.x,
            bullet_pos.y,
            50,
            25,
            150,
            sprite_path=os.path.join(BULLETS_PATH, "rocket.png"),
        )
        bullet.velocity = self.direction * 15
        bullets.append(bullet)

        return bullets
