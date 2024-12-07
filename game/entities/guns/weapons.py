import os

from game.entities.guns.bullets import Bullet, Grenade, BlowingBullet
from game.entities.game_object import GameObject
from geometry.Vector import Vector
from game.constants import ASSETS_PATH
import pygame as pg
import math
import random


BULLETS_PATH = os.path.join(ASSETS_PATH, "weapons", "bullets")

class Weapon(GameObject):
    def __init__(self, x, y, width, sprite_path):
        super().__init__(x, y, width=width, sprite_path=sprite_path)
        self.sprite = None
        self.kickback = 0
        self.direction = Vector(0, 0)
        self.dist = 30
        pass

    def get_bullet(self):
        pass

    def draw(self, screen, center):
        if not self.sprite:
            return
        angle = -math.atan2(self.direction.y, self.direction.x) / math.pi * 180
        pos, _, _ = self.convert_coordinates(center)
        rect = self.sprite.get_rect(center=pos.tuple)
        image = self.sprite
        if angle > 90 or angle < -90:
            image = pg.transform.flip(image, False, True)
        image = pg.transform.rotate(image, angle)

        screen.blit(image, rect)


class Pistol(Weapon):
    def get_bullet(self):
        bullet_pos = self.position + self.direction * self.dist / 2
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
    def get_bullet(self):
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
    def __init__(self, x, y, width, sprite_path):
        super().__init__(x, y, width, sprite_path)
        self.kickback = 20

    def get_bullet(self):
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


class Egg(Weapon):
    def get_bullet(self):
        bullets = []
        bullet_pos = self.position - self.direction * 60 + Vector(0, 60)
        bullet = Grenade(
            bullet_pos.x,
            bullet_pos.y,
            50,
            50,
            300,
            sprite_path=os.path.join(BULLETS_PATH, "egg.png"),
        )
        bullet.velocity = Vector(3 * (random.randint(0, 1) - 0.5) * 2, 0)
        bullets.append(bullet)
        return bullets

    def draw(self, screen, center):
        pass


class Kit(Weapon):
    def __init__(self, x, y, width, sprite_path, owner):
        super().__init__(x, y, width, sprite_path)
        self.hp = 100
        self.owner = owner

    def get_bullet(self):
        self.owner.hp += self.hp
