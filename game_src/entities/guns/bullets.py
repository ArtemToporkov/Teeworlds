import math
import pygame as pg

from game_src.entities.game_object import GameObject
from game_src.constants import GRAVITY, ASSETS_PATH
from os.path import join
from game_src.utils.enums import BulletData, BlowingBulletData, GameObjectData, TypeData

from geometry.vector import Vector


class Bullet(GameObject):
    def __init__(self, x, y, width, height, damage, sprite_path=None):
        super().__init__(x, y, width, height, sprite_path=sprite_path)
        self.damage = damage
        self.lifetime = 0
        self.blowing = False
        self.direction = self.velocity.normalize()
        self.animation_frames = [
            pg.image.load(join(ASSETS_PATH, 'weapons', 'bullets', 'explosion_animation', f"explosion_{i}.png"))
            for i in range(1, 8)
        ]

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
        from game_src.utils.serialization_tools import unpacking_path
        bullet = Bullet(
            x=data[GameObjectData.POSITION_X.value],
            y=data[GameObjectData.POSITION_Y.value],
            width=data[GameObjectData.WIDTH.value],
            height=data[GameObjectData.HEIGHT.value],
            sprite_path=unpacking_path(data[GameObjectData.SPRITE_PATH.value]),
            damage=data[BulletData.DAMAGE.value]
        )
        bullet.direction = Vector(*data[BulletData.DIRECTION.value])
        bullet.velocity = Vector(*data[GameObjectData.VELOCITY.value])
        return bullet



class BlowingBullet(Bullet):
    def __init__(self, x, y, width, height, damage, sprite_path=None):
        super().__init__(x, y, width, height, damage, sprite_path=sprite_path)
        self.radius = 150
        self.blowing = False
        self.number_animation_frame = 1

    def apply_forces(self):
        if not self.is_landed:
            self.velocity = self.velocity + Vector(0, GRAVITY) * 0.4

    def update(self):
        if self.blowing: return
        super().update()
        self.direction = self.velocity.normalize()

    def to_dict(self):
        data = super().to_dict()
        data[TypeData.TYPE.value] = type(self).__name__
        data.update({
            BlowingBulletData.RADIUS.value: self.radius
        })
        return data

    def draw(self, screen, center):
        # print(f'blowing: {self.blowing}')
        if self.blowing:
            if self.number_animation_frame < len(self.animation_frames):
                # print(f'frame: {self.number_animation_frame}')
                frame = self.animation_frames[int(self.number_animation_frame)]
                position = self.get_coordinates_offset_by_center(center)
                frame_rect = frame.get_rect(center=(position.x + self.width // 2, position.y + self.height // 2))
                screen.blit(frame, frame_rect.topleft)
                self.number_animation_frame += 0.25
                # pg.draw.circle(screen, (0, 0, 255), position.to_tuple(), self.radius) # рисует область взрыва
            else:
                self.alive = False
                self.blowing = False

        else:
            super().draw(screen, center)

    def interact(self, other):
        from game_src.entities.player import Player
        # self.alive = self.alive and not self.blowing
        if isinstance(other, Player) and self.intersects(other):
            self.blowing = True
        from game_src.entities.map.platform import Platform
        if isinstance(other, Platform) and self.intersects(other):
            self.blowing = True

    @staticmethod
    def from_dict(data):
        from game_src.utils.serialization_tools import unpacking_path
        bullet = BlowingBullet(
            x=data[GameObjectData.POSITION_X.value],
            y=data[GameObjectData.POSITION_Y.value],
            width=data[GameObjectData.WIDTH.value],
            height=data[GameObjectData.HEIGHT.value],
            sprite_path=unpacking_path(data[GameObjectData.SPRITE_PATH.value]),
            damage=data[BulletData.DAMAGE.value]
        )
        bullet.radius = data[BlowingBulletData.RADIUS.value]
        bullet.direction = Vector(*data[BulletData.DIRECTION.value])
        bullet.velocity = Vector(*data[GameObjectData.VELOCITY.value])
        return bullet
