import os

import pygame
from pathlib import Path

from game.entities.entity import Entity
from geometry.Vector import Vector
from enum import IntEnum, auto


class States(IntEnum):
    STANDING = auto()
    RUNNING_RIGHT = auto()
    RUNNING_LEFT = auto()
    JUMPING = auto()


class Player(Entity):
    def __init__(self, x, y, width, height):
        player_sprite_path = Path(__file__).parent.parent.parent / 'assets' / 'player' / 'standing.png'
        super().__init__(x, y, width, height, player_sprite_path)
        self.sprite = pygame.image.load(player_sprite_path)
        self.sprite = pygame.transform.scale(self.sprite, (width, height))
        self.state = States.STANDING

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
            case States.RUNNING_RIGHT | States.RUNNING_LEFT:
                frame = self.running_frames[self.current_running_frame]
                frame = pygame.transform.flip(frame, True, False) \
                    if self.state == States.RUNNING_LEFT \
                    else frame
                screen.blit(frame, (self.position.x, self.position.y, self.width, self.height))
                self._update_running_frame()
            case States.STANDING:
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
        for frame_file in os.listdir(frames_path):
            frame = pygame.image.load(frames_path / frame_file)
            frame = pygame.transform.scale(frame, (self.width, self.height))
            frames.append(frame)
        return frames

    def _update_running_frame(self) -> None:
        self.current_running_frame += 1
        if self.current_running_frame == 27:
            self.current_running_frame = 0

    def _update_jumping_frame(self) -> None:
        if self.state != States.JUMPING:
            self.current_jumping_frame = 0
        elif self.current_jumping_frame == 11:
            return
        else:
            self.current_jumping_frame += 1



