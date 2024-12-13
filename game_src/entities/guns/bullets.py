import math
import pygame as pg

from game_src.entities.game_object import GameObject
from game_src.constants import GRAVITY, ASSETS_PATH
from os.path import join
from game_src.utils.enums import BulletData, BlowingBulletData, GameObjectData, TypeData

from game_src.entities.guns.effects import Effect
from geometry.vector import Vector


class Bullet(GameObject):
    def __init__(self, x, y, width, height, damage, sprite_path=None):
        super().__init__(x, y, width, height, sprite_path=sprite_path)
        self.damage = damage
        self.lifetime = 0
        self.blowing = False
        self.direction = self.velocity.normalize()

    def apply_forces(self):
        pass

    def update(self):
        super().update()
        self.direction = self.velocity.normalize()
        self.lifetime += 1
        if self.lifetime > 300:
            self.alive = False

    def interact(self, other):
        from game_src.entities.player import Player
        self.alive = self.alive and not self.blowing
        if isinstance(other, Player) and self.intersects(other):
            self.alive = False
        from game_src.entities.map.platform import Platform
        if isinstance(other, Platform) and self.intersects(other):
            self.alive = False

    def draw(self, screen, center):
        if self.image is None:
            super().draw(screen, center)
            return
        angle = -math.atan2(self.direction.y, self.direction.x) / math.pi * 180
        rotated_image = pg.transform.rotate(self.image, angle)
        new_position = self.get_coordinates_offset_by_center(center)
        screen.blit(rotated_image, (new_position.x, new_position.y, self.width, self.height))

    def to_dict(self):
        data = super().to_dict()
        data[TypeData.TYPE.value] = type(self).__name__
        data.update({
            BulletData.DAMAGE.value: self.damage,
            BulletData.DIRECTION.value: self.direction.to_tuple(),
        })

        return data

    @staticmethod
    def from_dict(data):
        bullet = Bullet(
            x=data[GameObjectData.POSITION_X.value],
            y=data[GameObjectData.POSITION_Y.value],
            width=data[GameObjectData.WIDTH.value],
            height=data[GameObjectData.HEIGHT.value],
            sprite_path=data[GameObjectData.SPRITE_PATH.value],
            damage=data[BulletData.DAMAGE.value]
        )
        bullet.direction = Vector(*data[BulletData.DIRECTION.value])
        bullet.velocity = Vector(*data[GameObjectData.VELOCITY.value])
        return bullet



class BlowingBullet(Bullet):
    def __init__(self, x, y, width, height, damage, sprite_path=None):
        super().__init__(x, y, width, height, damage, sprite_path=sprite_path)
        self.radius = 250
        self.blowing = False
        self.animation_frame = 0

    def apply_forces(self):
        if not self.is_landed:
            self.velocity = self.velocity + Vector(0, GRAVITY) * 0.4

    def update(self):
        super().update()
        self.direction = self.velocity.normalize()
        self.frames += 1

    def to_dict(self):
        data = super().to_dict()
        data[TypeData.TYPE.value] = type(self).__name__
        data.update({
            BlowingBulletData.RADIUS.value: self.radius
        })
        return data

    def draw(self, screen, center):
        if self.blowing:
            self.animation_frame += 1

        else:
            super().draw(screen, center)

    def interact(self, other):
        from game_src.entities.player import Player
        self.alive = self.alive and not self.blowing
        if isinstance(other, Player) and self.intersects(other):
            self.alive = False
            self.blowing = True
        from game_src.entities.map.platform import Platform
        if isinstance(other, Platform) and self.intersects(other):
            self.alive = False
            self.blowing = True

    @staticmethod
    def from_dict(data):
        bullet = BlowingBullet(
            x=data[GameObjectData.POSITION_X.value],
            y=data[GameObjectData.POSITION_Y.value],
            width=data[GameObjectData.WIDTH.value],
            height=data[GameObjectData.HEIGHT.value],
            sprite_path=data[GameObjectData.SPRITE_PATH.value],
            damage=data[BulletData.DAMAGE.value]
        )
        bullet.radius = data[BlowingBulletData.RADIUS.value]
        bullet.direction = Vector(*data[BulletData.DIRECTION.value])
        bullet.velocity = Vector(*data[GameObjectData.VELOCITY.value])
        return bullet


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

    def interact(self, other):
        pass