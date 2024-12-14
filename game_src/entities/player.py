import math
import os
import pygame as pg

import pygame
from pathlib import Path

from pygame.key import ScancodeWrapper

from game_src.constants import WINDOW_WIDTH, WINDOW_HEIGHT, GRAVITY, JUMP_STRENGTH, MAX_HP, \
    MAX_DISTANCE_TO_CENTRE_FOR_PLAYER, MAP_WIDTH, MAP_HEIGHT
from game_src.constants import WINDOW_WIDTH, WINDOW_HEIGHT, GRAVITY, JUMP_STRENGTH, HITBOXES_MODE, DELTA_FOR_COLLISIONS, \
    MAX_HOOK_LENGTH
from game_src.constants import MOVEMENT_SPEED, ASSETS_PATH
from game_src.entities.game_object import GameObject
from game_src.entities.guns.bullets import Grenade, Bullet
from game_src.entities.guns.weapons import Pistol, ShotGun, Rocket, MedKit
from game_src.utils.enums import PlayerStates, Collisions, PlayerData, GameObjectData, TypeData, get_state_by_value
from game_src.entities.guns.weapons import Pistol, ShotGun, Rocket
from game_src.utils.enums import PlayerStates, Collisions, PlayerData, GameObjectData, TypeData
from geometry.vector import Vector


class Player(GameObject):
    def __init__(self, x, y, width, height):
        player_sprite_path = Path(__file__).parent.parent.parent / 'assets' / 'player' / 'standing.png'
        super().__init__(x, y, width=width, height=height, sprite_path=player_sprite_path)
        self.spawn_position = Vector(x, y)
        self.sprite = pygame.image.load(player_sprite_path)
        self.sprite = pygame.transform.scale(self.sprite, (width, height))
        self.state = PlayerStates.STANDING
        self.looking_direction = PlayerStates.LOOKING_RIGHT
        self.move_force_vector = Vector(0, 0)
        self.jumped = True
        self.in_air = False
        self.hook_position = None
        self.is_landed = False
        self.hook_vector = None
        self.hook_buffer = Vector(0, 0)

        self.weapons = [
            Pistol(0, 0, 50, 50, os.path.join(ASSETS_PATH, "weapons", "pistol.png")),
            ShotGun(0, 0, 50, 50, os.path.join(ASSETS_PATH, "weapons", "shotgun.png")),
            Rocket(0, 0, 75, 75, os.path.join(ASSETS_PATH, "weapons", "rpg.png")),
            MedKit(0, 0, 75, 75, os.path.join(ASSETS_PATH, "weapons", "medkit.png"), 50)
        ]
        self.current_weapon = 0
        self.cooldown = 30

        self.hp = MAX_HP
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
        if self.hook_position:
            self._draw_hook(screen)
        if HITBOXES_MODE:
            self._draw_move_force_vector(screen)
        self.weapons[self.current_weapon].draw(screen, center)

        hp_bar = (new_position - Vector(0, 15)).to_tuple() + (self.width * self.hp / MAX_HP, 12)
        color = (255, 0, 0)
        pg.draw.rect(screen, color, hp_bar)

        match self.state:
            case PlayerStates.RUNNING:
                frame = self.running_frames[self.current_running_frame]
                frame = pygame.transform.flip(frame, True, False) \
                    if self.looking_direction == PlayerStates.LOOKING_LEFT \
                    else frame
                screen.blit(frame, (new_position.x, new_position.y, self.width, self.height))
                self._update_running_frame()
            case PlayerStates.IN_AIR:
                frame = self.jumping_frames[self.current_jumping_frame]
                frame = pygame.transform.flip(frame, True, False) \
                    if self.looking_direction == PlayerStates.LOOKING_LEFT \
                    else frame
                screen.blit(frame, (new_position.x, new_position.y, self.width, self.height))
                self._update_jumping_frame()
            case PlayerStates.STANDING:
                sprite = self.sprite if self.looking_direction == PlayerStates.LOOKING_RIGHT \
                    else pygame.transform.flip(self.sprite, True, False)
                screen.blit(sprite, (new_position.x, new_position.y, self.width, self.height))
            case _:
                pass

    def _draw_move_force_vector(self, screen: pygame.display) -> None:
        pygame.draw.line(screen, (255, 255, 255),
                         (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),
                         (10 * self.move_force_vector.x + WINDOW_WIDTH / 2,
                          10 * self.move_force_vector.y + WINDOW_HEIGHT / 2))

    def update(self):
        # print(f'position: {self.position}')
        # print(f'force vector: {self.move_force_vector}')
        self.cooldown -= 1
        if self.hp <= 0:
            self.alive = False
            self.hp = 100
        self.weapons[self.current_weapon].position = self.position + self.look_direction * 60
        self.weapons[self.current_weapon].direction = self.look_direction
        if self.position.x > MAP_WIDTH or self.position.x < 0 or self.position.y < 0 or self.position.y > MAP_WIDTH:
            self.alive = False

    def interact(self, other):
        from game_src.entities.guns.bullets import Bullet, BlowingBullet
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
                    # other.alive = False
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
        if self.cooldown < 0:
            self.cooldown = 30
            weapon = self.weapons[self.current_weapon]
            if isinstance(weapon, MedKit):
                self.hp = min(self.hp + weapon.get_bullets(), MAX_HP)
                self.current_weapon = 0
                self.weapons.remove(weapon)
                return []

            return weapon.get_bullets()

    def process_keys_and_move(
            self, pressed_keys: ScancodeWrapper | list[bool], mouse_pos: tuple[int, int], platforms: list['Platform']
    ) -> None:
        a_pressed, d_pressed, w_pressed = pressed_keys[pygame.K_a], pressed_keys[pygame.K_d], pressed_keys[pygame.K_w]
        shift_pressed = pressed_keys[pygame.K_LSHIFT]

        if shift_pressed:
            self._handle_hook(platforms, mouse_pos, self.hook_position is not None)
            if self.hook_vector:
                self.move_force_vector += self.hook_vector
                self.move_force_vector = Vector(
                    max(-MOVEMENT_SPEED, self.move_force_vector.x) if self.move_force_vector.x < 0
                    else min(MOVEMENT_SPEED, self.move_force_vector.x),
                    max(-MOVEMENT_SPEED, self.move_force_vector.y) if self.move_force_vector.y < 0
                    else min(MOVEMENT_SPEED, self.move_force_vector.y)
                )
        else:
            self.hook_position = None
            self.hook_vector = None

        if all(not pressed for pressed in (a_pressed, d_pressed, w_pressed, shift_pressed)) and self.is_landed:
            self.state = PlayerStates.STANDING
            self.move_force_vector = Vector(0, 0)
            return

        if self.hook_vector is None:
            if a_pressed:
                self.move_force_vector = Vector(
                    max(self.move_force_vector.x - 1, -MOVEMENT_SPEED),
                    self.move_force_vector.y
                )
            elif d_pressed:
                self.move_force_vector = Vector(
                    min(self.move_force_vector.x + 1, MOVEMENT_SPEED),
                    self.move_force_vector.y
                )

            if w_pressed and not self.jumped:
                self.move_force_vector = Vector(
                    self.move_force_vector.x,
                    self.move_force_vector.y - JUMP_STRENGTH
                )
                self.jumped = True
                self.is_landed = False

            if not self.is_landed:
                self.move_force_vector = Vector(
                    self.move_force_vector.x,
                    min(self.move_force_vector.y + GRAVITY, 3 * MOVEMENT_SPEED)
                )

        is_landed_flag = False
        for platform in platforms:
            collisions = platform.get_collisions(self, self.move_force_vector)
            x_collision = False
            if collisions[Collisions.X_LEFT] is not None and self.move_force_vector.x < 0:
                self.position = Vector(
                    platform.top_right.x + DELTA_FOR_COLLISIONS,
                    self.position.y
                )
                x_collision = True
            elif collisions[Collisions.X_RIGHT] is not None and self.move_force_vector.x > 0:
                self.position = Vector(
                    platform.top_left.x - DELTA_FOR_COLLISIONS - self.width,
                    self.position.y
                )
                x_collision = True

            y_collision = False
            if collisions[Collisions.Y_DOWN] is not None and self.move_force_vector.y > 0:
                self.position = Vector(
                    self.position.x,
                    platform.top_left.y - DELTA_FOR_COLLISIONS - self.height
                )
                self.is_landed = True
                self.jumped = False
                y_collision = True
            if collisions[Collisions.Y_UP] is not None and self.move_force_vector.y < 0:
                self.position = Vector(
                    self.position.x,
                    platform.bottom_left.y + DELTA_FOR_COLLISIONS
                )
                y_collision = True

            self.move_force_vector = Vector(
                self.move_force_vector.x if not x_collision else 0,
                self.move_force_vector.y if not y_collision else 0
            )

            is_landed_flag = is_landed_flag or platform.move_and_check_collisions(self, 0, 5)
            self.is_landed = is_landed_flag
        self._set_looking_direction_for_animations(a_pressed, d_pressed, w_pressed, shift_pressed, self.is_landed)
        self.move(self.move_force_vector)

    def _set_looking_direction_for_animations(
            self,
            a_pressed: bool,
            d_pressed: bool,
            w_pressed: bool,
            shift_pressed: bool,
            is_landed: bool):
        if not is_landed or w_pressed:
            self.state = PlayerStates.IN_AIR
            if a_pressed:
                self.looking_direction = PlayerStates.LOOKING_LEFT
            if d_pressed:
                self.looking_direction = PlayerStates.LOOKING_RIGHT
            print(self.looking_direction, self.state)
            return
        if a_pressed:
            self.state = PlayerStates.RUNNING
            self.looking_direction = PlayerStates.LOOKING_LEFT
        elif d_pressed:
            self.state = PlayerStates.RUNNING
            self.looking_direction = PlayerStates.LOOKING_RIGHT

    def _handle_hook(self, platforms: list["Platform"], mouse_pos: tuple[int, int], already_hooked: bool):
        self.hook_position = (
                Vector(mouse_pos[0], mouse_pos[1]) - Vector(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        ).normalize() * MAX_HOOK_LENGTH if not already_hooked else self.hook_position - self.position
        self.hook_vector = Vector(self.hook_position.x, self.hook_position.y)  # позиция относительно (0,0)
        self.hook_position += self.position  # позиция относительно игрока
        hook_parts_count = 100
        new_x, new_y = None, None
        for i in range(1, hook_parts_count):
            # сужаем крюк, всё слишком дискретно, зато работает безотказно
            new = self.hook_vector.normalize() * i * MAX_HOOK_LENGTH / (hook_parts_count - 1) + self.position
            for platform in platforms:
                if new_x is not None and new_y is not None:
                    break
                # учитываем то, что позиция закреплена на левым верхним углом игрока
                if platform.top_left.x <= new.x + self.width / 2 <= platform.top_right.x \
                        and platform.top_left.y <= new.y + self.height / 2 <= platform.bottom_right.y:
                    new_x, new_y = new.x, new.y
        if new_x is None and new_y is None:
            self.hook_position = None
            self.hook_vector = None
        else:
            self.hook_position = Vector(new_x, new_y)
            self.hook_vector = (self.hook_position - self.position).normalize()

    def _draw_hook(self, screen: pygame.display) -> None:
        pygame.draw.line(
            screen,
            (255, 255, 255),
            (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),
            (self.hook_position.x + WINDOW_WIDTH / 2 - self.position.x, self.hook_position.y + WINDOW_HEIGHT / 2 - self.position.y),
            2,
        )

    def _update_running_frame(self) -> None:
        self.current_running_frame += 1
        if self.current_running_frame == 27:
            self.current_running_frame = 0

    def _update_jumping_frame(self) -> None:
        if self.state != PlayerStates.IN_AIR or not self.jumped:
            self.current_jumping_frame = 0
        elif self.current_jumping_frame == 11:
            return
        else:
            self.current_jumping_frame += 1

    def update_from_wrap(self, player):
        self.position = player.position
        self.velocity = player.velocity
        self.look_direction = player.look_direction
        self.width = player.width
        self.height = player.height
        self.sprite_path = player.sprite_path
        self.state = player.state
        self.current_weapon = player.current_weapon
        # if not player.hook_end:
        #     self.hook = None
        # elif not self.hook:
        #     self.hook = Hook(self, wrap.hook_end)

    def to_dict(self):
        data = super().to_dict()
        data[TypeData.TYPE.value] = type(self).__name__
        data.update({
            PlayerData.STATE.value: self.state.value,
            PlayerData.CURRENT_WEAPON.value: self.current_weapon,
            PlayerData.HP.value: self.hp,
        })

        # if self.hook_position:
        #     data[PlayerData.HOOK_POSITION.value] = self.hook_position
        # if self.hook_position:
        #     data[PlayerData.HOOK_POSITION]
        return data

    @staticmethod
    def from_dict(data):
        player = Player(
            x=data[GameObjectData.POSITION_X.value],
            y=data[GameObjectData.POSITION_Y.value],
            width=data[GameObjectData.WIDTH.value],
            height=data[GameObjectData.HEIGHT.value],
        )
        player.velocity = Vector(*data[GameObjectData.VELOCITY.value])
        player.look_direction = Vector(*data[GameObjectData.DIRECTION.value])
        player.state = get_state_by_value(data[PlayerData.STATE.value])
        player.current_weapon = data[PlayerData.CURRENT_WEAPON.value]
        player.hp = data[PlayerData.HP.value]
        # player.hook_position = data[PlayerData.HOOK_POSITION.value]

        return player
