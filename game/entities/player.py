import os
import pygame as pg

import pygame
from pathlib import Path

from pygame.key import ScancodeWrapper

from game.constants import WINDOW_WIDTH, WINDOW_HEIGHT, GRAVITY, JUMP_STRENGTH
from game.constants import MOVEMENT_SPEED, ASSETS_PATH
from game.entities.game_object import GameObject
from game.entities.guns.bullets import Grenade, Bullet
from game.entities.guns.weapons import Pistol, ShotGun, Rocket
from game.utils.enums import PlayerStates, Collisions, PlayerData, GameObjectData, TypeData
from geometry.vector import Vector


class Player(GameObject):
    def __init__(self, x, y, width, height):
        player_sprite_path = Path(__file__).parent.parent.parent / 'assets' / 'player' / 'standing.png'
        super().__init__(x, y, width=width, height=height, sprite_path=player_sprite_path)
        self.sprite = pygame.image.load(player_sprite_path)
        self.sprite = pygame.transform.scale(self.sprite, (width, height))
        self.state = PlayerStates.STANDING
        self.move_force_vector = Vector(0, 0)
        self.jumped = False
        self.in_air = False

        self.weapons = [
            Pistol(0, 0, 50, 50, os.path.join(ASSETS_PATH, "weapons", "pistol.png")),
            ShotGun(0, 0, 50, 50, os.path.join(ASSETS_PATH, "weapons", "shotgun.png")),
            Rocket(0, 0, 75, 75, os.path.join(ASSETS_PATH, "weapons", "rpg.png")),
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

    def draw(self, screen: pygame.display, center: GameObject) -> None:
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
            case PlayerStates.JUMPING:
                frame = self.jumping_frames[self.current_jumping_frame]
                frame = pygame.transform.flip(frame, True, False) \
                    if self.state == PlayerStates.RUNNING_LEFT \
                    else frame
                screen.blit(frame, (new_position.x, new_position.y, self.width, self.height))
                self._update_jumping_frame()
            case PlayerStates.STANDING:
                screen.blit(self.sprite, (new_position.x, new_position.y, self.width, self.height))
            case _:
                pass

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
        self.weapons[self.current_weapon].position = self.position + self.look_direction * 60
        self.weapons[self.current_weapon].direction = self.look_direction
        if self.position.length() > 10000:
            self.hp -= 1000

        # for buff in self.buffs:
        #     if buff.ended:
        #         buff.delete()
        #         self.buffs.remove(buff)
        #     else:
        #         buff.update()

    def interact(self, other):
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

    def move_by_coordinates(self, dx, dy):
        self.position += Vector(dx, dy)

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

    def set_look_direction(self) -> None:
        self.look_direction = (
                Vector(*pg.mouse.get_pos()) - Vector(WINDOW_WIDTH, WINDOW_HEIGHT) / 2
        ).normalize()

    def shoot(self) -> list[Bullet]:
        bullets = self.weapons[self.current_weapon].get_bullets()
        return bullets

    def process_keys_and_move(self, pressed_keys: ScancodeWrapper | list[bool], platforms: list['Platform']) -> None:
        a_pressed, d_pressed, w_pressed = pressed_keys[pygame.K_a], pressed_keys[pygame.K_d], pressed_keys[pygame.K_w]

        if d_pressed:
            self._handle_movement(platforms, MOVEMENT_SPEED, Collisions.X_RIGHT, PlayerStates.RUNNING_RIGHT)
        elif a_pressed:
            self._handle_movement(platforms, -MOVEMENT_SPEED, Collisions.X_LEFT, PlayerStates.RUNNING_LEFT)
        else:
            self._stay()
        self._handle_gravity(platforms)
        if w_pressed and not self.jumped:
            self._handle_jump(platforms)
        self.move(self.move_force_vector)

    def _handle_movement(self, platforms, speed, collision_type, state):
        collisions = self.predict_collisions(platforms, self._get_changed_move_vector(x=speed))
        if not collisions[collision_type]:
            self._change_move_vector(x=speed)
            self.state = state if not self.jumped else PlayerStates.JUMPING
        else:
            self._stay()

    def _handle_gravity(self, platforms):
        current_collisions = self.predict_collisions(platforms, self.move_force_vector)
        if not current_collisions[Collisions.Y_DOWN]:
            collisions = self.predict_collisions(platforms, self._get_changed_move_vector(
                y=self.move_force_vector.y + GRAVITY
            ))
            if not collisions[Collisions.Y_DOWN]:
                self._change_move_vector(y=self.move_force_vector.y + GRAVITY)
            else:
                self._change_move_vector(y=0)
                self.jumped = False
        else:
            self._change_move_vector(y=0)
        if current_collisions[Collisions.Y_UP]:
            self._change_move_vector(y=0)

    def _handle_jump(self, platforms):
        collisions = self.predict_collisions(platforms, self._get_changed_move_vector(y=-JUMP_STRENGTH))
        if not collisions[Collisions.Y_UP]:
            self._change_move_vector(y=-JUMP_STRENGTH)
            self.state = PlayerStates.JUMPING
            self.jumped = True
        else:
            self._change_move_vector(y=0)

    def _stay(self) -> None:
        self.state = PlayerStates.STANDING if not self.jumped else PlayerStates.JUMPING
        self._change_move_vector(x=0)

    def _change_move_vector(self, x: float = None, y: float = None) -> None:
        self.move_force_vector = Vector(
            self.move_force_vector.x if x is None else x,
            self.move_force_vector.y if y is None else y,
        )

    def _get_changed_move_vector(self, x: float = None, y: float = None) -> Vector:
        return Vector(
            self.move_force_vector.x if x is None else x,
            self.move_force_vector.y if y is None else y,
        )

    def _add_to_move_vector(self, dx: float = None, dy: float = None) -> None:
        self.move_force_vector += Vector(dx if dx else 0, dy if dy else 0)

    def _update_running_frame(self) -> None:
        self.current_running_frame += 1
        if self.current_running_frame == 27:
            self.current_running_frame = 0

    def _update_jumping_frame(self) -> None:
        if self.state != PlayerStates.JUMPING or not self.jumped:
            self.current_jumping_frame = 0
        elif self.current_jumping_frame == 11:
            return
        else:
            self.current_jumping_frame += 1

    def to_dict(self):
        data = super().to_dict()
        data[TypeData.TYPE.value] = f"{self.__class__.__module__}.{self.__class__.__name__}"
        data.update({
            PlayerData.STATE.value: self.state,
            PlayerData.CURRENT_WEAPON.value: self.current_weapon,
        })
        return data

    @staticmethod
    def from_dict(data):
        player = Player(
            x=data[GameObjectData.POSITION_X.value],
            y=data[GameObjectData.POSITION_Y.value],
            width=data[GameObjectData.WIDTH.value],
            height=data[GameObjectData.HEIGHT.value],
        )
        player.velocity = data[GameObjectData.VELOCITY.value]
        player.look_direction = data[GameObjectData.DIRECTION.value]
        player.state = data[PlayerData.STATE.value]
        player.current_weapon = data[PlayerData.CURRENT_WEAPON.value]
        return player
