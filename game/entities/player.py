import os
import pygame as pg

import pygame
from pathlib import Path

from game.constants import BACKGROUND_HEIGHT, BACKGROUND_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT
from game.constants import MOVEMENT_SPEED, ASSETS_PATH
from game.entities.game_object import GameObject
from game.entities.guns.bullets import Grenade
from game.entities.guns.weapons import Pistol, ShotGun, Rocket, Egg
from game.enums import PlayerStates
from geometry.Vector import Vector
from enum import IntEnum, auto



class Player(GameObject):
    def __init__(self, x, y, width, height):
        player_sprite_path = Path(__file__).parent.parent.parent / 'assets' / 'player' / 'standing.png'
        super().__init__(x, y, width=width, height=height, sprite_path=player_sprite_path)
        self.sprite = pygame.image.load(player_sprite_path)
        self.sprite = pygame.transform.scale(self.sprite, (width, height))
        self.state = PlayerStates.STANDING
        self.movement_speed = MOVEMENT_SPEED
        self.move_force_vector = Vector(0, MOVEMENT_SPEED)
        self.jumped = False

        self.weapons = [
            Pistol(0, 0, 50, os.path.join(ASSETS_PATH, "weapons", "pistol.png")),
            ShotGun(0, 0, 50, os.path.join(ASSETS_PATH, "weapons", "shotgun.png")),
            Rocket(0, 0, 75, os.path.join(ASSETS_PATH, "weapons", "rpg.png")),
            Egg(0, 0, 50, None),
        ]
        self.current_weapon = 0
        self.cooldown = 30

        self.hp = 100 + 100
        self.alive = True

        self.current_running_frame = 0
        self.running_frames = self.create_frames_list(
            Path(__file__).parent.parent.parent / 'assets' / 'player' / 'running'
        )

        self.current_jumping_frame = 0
        self.jumping_frames = self.create_frames_list(
            Path(__file__).parent.parent.parent / 'assets' / 'player' / 'jumping'
        )

    def draw(self, screen: pygame.display, center: Vector):
        new_position = self.get_coordinates_offset_by_center(center)
        self.weapons[self.current_weapon].draw(screen, center)
        match self.state:
            case PlayerStates.RUNNING_RIGHT | PlayerStates.RUNNING_LEFT:
                frame = self.running_frames[self.current_running_frame]
                frame = pygame.transform.flip(frame, True, False) \
                    if self.state == PlayerStates.RUNNING_LEFT \
                    else frame
                screen.blit(frame, (new_position.x, new_position.y, self.width, self.height))
                self._update_running_frame()
            case PlayerStates.STANDING:
                screen.blit(self.sprite, (new_position.x, new_position.y, self.width, self.height))
            case _:
                pass

    def change_move_vector(self, x: int = None, y: int = None) -> None:
        self.move_force_vector = Vector(
            self.move_force_vector.x if not x else x,
            self.move_force_vector.y if not y else y,
        )

    def update(self):
        # super().update()
        self.cooldown -= 1
        # if self.hook:
        #     self.hook.update()
        # if not self.is_landed:
        #     self.state = "jump"         МОЖНО ИСПОЛЬЗОВАТЬ ДЛЯ АНИМАЦИИ ВМЕСТО ТОГО ЧТОБЫ ТРЕЧИТЬ В GAME
        # if self.is_landed:
        #     self.jump_count = 0
        # if self.hp < -1:
        #     self.die_count += 1
        #     if self.die_count > 10:
        #         self.pashalka()
        #     self.alive = False
        #     self.hp = 100 + 100
        # if self.hp < 200:
        #     self.hp += 8 / 60
        self.weapons[self.current_weapon].position = self.position + self.direction * 60
        self.weapons[self.current_weapon].direction = self.direction
        if self.position.length() > 10000:
            self.hp -= 1000

        # for buff in self.buffs:
        #     if buff.ended:
        #         buff.delete()
        #         self.buffs.remove(buff)
        #     else:
        #         buff.update()

    def act(self, other):
        # проходит по всем объектам с которыми может взаимодействовать игрок
        # Ну и взаимодействует
        from game.entities.guns.bullets import Bullet, BlowingBullet

        if self is other:
            return
        intersecting = self.intersects(other)
        if isinstance(other, Player):
            if intersecting:
                vec = (self.position - other.position).normalize() * 5
                if vec.length() == 0:
                    vec = Vector(1, 0)
                self.velocity = vec

        elif isinstance(other, Bullet):
            if isinstance(other, BlowingBullet):
                if intersecting:
                    other.blowing = True
                    other.alive = False
                    self.hp -= other.damage
                if (
                    other.blowing
                    and (self.position - other.position).length() < other.radius
                ):
                    self.hp -= other.damage
            if isinstance(other, Grenade):
                if (
                    other.blowing
                    and (self.position - other.position).length() < other.radius
                ):
                    self.hp -= other.damage
            elif intersecting:
                other.alive = False
                self.hp -= other.damage

        # elif isinstance(other, Buff):
        #     if intersecting:
        #         self.add_buff(other)

    def move(self):
        self.position += self.move_force_vector
        self._calm_down_force_vector()

    def move_by_coordinates(self, dx, dy):
        self.position += Vector(dx, dy)

    def jump(self) -> None:
        pass

    def create_frames_list(self, frames_path: Path) -> list[pygame.image]:
        frames = []
        for frame_file in sorted(
                os.listdir(frames_path), key=lambda file_name: int(file_name.split('.')[0])
        ):  # сортировка по номеру кадра, название файла: [номер кадра].png
            # print(frame_file)
            frame = pygame.image.load(frames_path / frame_file)
            frame = pygame.transform.scale(frame, (self.width, self.height))
            frames.append(frame)
        return frames

    def _update_running_frame(self) -> None:
        self.current_running_frame += 1
        if self.current_running_frame == 27:
            self.current_running_frame = 0

    def _update_jumping_frame(self) -> None:
        if self.state != PlayerStates.JUMPING:
            self.current_jumping_frame = 0
        elif self.current_jumping_frame == 11:
            return
        else:
            self.current_jumping_frame += 1

    def set_direction(self):
        self.direction = (
            Vector(*pg.mouse.get_pos()) - Vector(WINDOW_WIDTH, WINDOW_HEIGHT) / 2
        ).normalize()

    def _calm_down_force_vector(self) -> None:
        self.move_force_vector = Vector(
            self._calm_down_x(self.move_force_vector.x),
            self._calm_down_y(self.move_force_vector.y)
        )

    @staticmethod
    def _calm_down_x(coordinate: float) -> float:
        if coordinate > 0:
            coordinate -= 1
        elif coordinate < 0:
            coordinate += 1
        return coordinate

    @staticmethod
    def _calm_down_y(coordinate: float) -> float:
        if coordinate < 2*MOVEMENT_SPEED:
            coordinate += 1
        return coordinate



    def shoot(self):
        if self.cooldown < 0:
            self.coldown = 30
            bullets = self.weapons[self.current_weapon].get_bullet()
            self.velocity += (
                -self.direction * self.weapons[self.current_weapon].kickback
            )
            return bullets
        return []