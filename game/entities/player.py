import os

import pygame
from pathlib import Path

from game.constants import MOVEMENT_SPEED
from game.entities.game_object import GameObject
from game.enums import PlayerStates
from geometry.Vector import Vector
from enum import IntEnum, auto



class Player(GameObject):
    def __init__(self, x, y, width, height):
        player_sprite_path = Path(__file__).parent.parent.parent / 'assets' / 'player' / 'standing.png'
        super().__init__(x, y, width, height, player_sprite_path)
        self.sprite = pygame.image.load(player_sprite_path)
        self.sprite = pygame.transform.scale(self.sprite, (width, height))
        self.state = PlayerStates.STANDING
        self.movement_speed = MOVEMENT_SPEED

        self.current_running_frame = 0
        self.running_frames = self.create_frames_list(
            Path(__file__).parent.parent.parent / 'assets' / 'player' / 'running'
        )

        self.current_jumping_frame = 0
        self.jumping_frames = self.create_frames_list(
            Path(__file__).parent.parent.parent / 'assets' / 'player' / 'jumping'
        )

    def draw(self, screen: pygame.display):
        match self.state:
            case PlayerStates.RUNNING_RIGHT | PlayerStates.RUNNING_LEFT:
                frame = self.running_frames[self.current_running_frame]
                frame = pygame.transform.flip(frame, True, False) \
                    if self.state == PlayerStates.RUNNING_LEFT \
                    else frame
                screen.blit(frame, (self.position.x, self.position.y, self.width, self.height))
                self._update_running_frame()
            case PlayerStates.STANDING:
                screen.blit(self.sprite, (self.position.x, self.position.y, self.width, self.height))
            case _:
                pass

    def move_left(self) -> None:
        self.move(Vector(-self.movement_speed, 0))

    def move_right(self) -> None:
        self.move(Vector(self.movement_speed, 0))

    def jump(self) -> None:
        pass

    def create_frames_list(self, frames_path: Path) -> list[pygame.image]:
        frames = []
        for frame_file in sorted(
                os.listdir(frames_path), key=lambda file_name: int(file_name.split('.')[0])
        ):  # сортировка по номеру кадра, название файла: [номер кадра].png
            print(frame_file)
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



