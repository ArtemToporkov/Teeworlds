import math
import random
import pygame as pg

from game.entities.game_object import GameObject
from game.constants import GRAVITY, ASSETS_PATH
from os.path import join

from game.entities.guns.effects import Effect
from geometry.Vector import Vector


class Bullet(GameObject):
    def __init__(self, x, y, width, height, damage, sprite_path=None):
        super().__init__(x, y, width, height, sprite_path=sprite_path)
        self.damage = damage
        self.lifetime = 0
        self.blowing = False

    def apply_forces(self):
        pass

    def update(self):
        super().update()
        # print('x:', self.position.x,'y:',self.position.y)
        self.direction = self.velocity.normalize()
        self.lifetime += 1
        if self.lifetime > 300:
            self.alive = False

    def act(self, other):
        from game.entities.player import Player
        self.alive = self.alive and not self.blowing
        if isinstance(other, Player) and self.intersects(other):
            self.alive = False


    def collide(self, map):
        for corner in self.corners:
            if (
                corner // map.tile_size * map.tile_size
                + Vector(map.tile_size / 2, map.tile_size / 2)
            ).tuple in map.blocks.keys():
                self.blowing = True

    def draw(self, screen, center):
        if self.image is None:
            super().draw(screen, center)
            return
        angle = -math.atan2(self.direction.y, self.direction.x) / math.pi * 180
        rotated_image = pg.transform.rotate(self.image, angle)
        pos, top_left, _ = self.convert_coordinates(center)
        rect = rotated_image.get_rect(center=pos.tuple)
        if self.sprite_path is not None:
            screen.blit(rotated_image, rect)


class BlowingBullet(Bullet):
    def __init__(self, x, y, width, height, damage, sprite_path=None):
        super().__init__(x, y, width, height, damage, sprite_path=sprite_path)
        self.radius = 250
        self.blowing = False

    def apply_forces(self):
        if not self.is_landed:
            self.velocity = self.velocity + GRAVITY * 0.4

    def update(self):
        super().update()
        self.direction = self.velocity.normalize()
        self.frames += 1


class Grenade(Bullet):
    def __init__(self, x, y, width, height, damage, sprite_path=None):
        super().__init__(x, y, width, height, damage, sprite_path=sprite_path)
        self.radius = 250
        self.blowing = False

    def apply_forces(self):
        if not self.is_landed:
            self.velocity = self.velocity + GRAVITY * 0.4

    def update(self):
        super().update()
        if self.velocity.length() > 10:
            self.velocity = self.velocity.normalize() * self.velocity.length()
        self.direction = self.velocity.normalize()
        self.frames += 1
        if self.lifetime > 299:
            self.blowing = True

    def act(self, other):
        pass

    def collide(self, map):
        for corner in self.corners:
            if (
                corner // map.tile_size * map.tile_size
                + Vector(map.tile_size / 2, map.tile_size / 2)
            ).tuple in map.blocks.keys():
                self.alive = False
        self.move(self.velocity.x, 0)
        for corner in self.corners:
            key = (
                corner // map.tile_size * map.tile_size
                + Vector(map.tile_size / 2, map.tile_size / 2)
            ).tuple
            block = map.blocks.get(key)
            if block is not None:
                self.move(-self.velocity.x, 0)
                self.velocity.x *= -1 * 0.8
                self.velocity.y *= 0.7
                break
        else:
            self.move(-self.velocity.x, 0)

        self.move(0, self.velocity.y)
        for corner in self.corners:
            key = (
                corner // map.tile_size * map.tile_size
                + Vector(map.tile_size / 2, map.tile_size / 2)
            ).tuple
            block = map.blocks.get(key)
            if block is not None:
                self.move(0, -self.velocity.y)
                self.velocity.y = -self.velocity.y * 0.5
                self.velocity.x *= 0.9
                break
        else:
            self.move(0, -self.velocity.y)

    def get_particle(self):
        if self.blowing:
            return Effect(
                self.position.x,
                self.position.y,
                400,
                400,
                animation_path=join(ASSETS_PATH, "particles", "explosion-1.png"),
            )

    def draw(self, screen, center):
        if self.image is None:
            super().draw(screen, center)
            return
        pos, top_left, _ = self.convert_coordinates(center)
        rect = self.image.get_rect(center=pos.tuple)
        if self.sprite_path is not None:
            screen.blit(self.image, rect)
