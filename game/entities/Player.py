import pygame
from pathlib import Path

from game.entities.Entity import Entity
from geometry.Vector import Vector
from enum import IntEnum


class States(IntEnum):
    STANDING = 0
    RUNNING_RIGHT = 1
    RUNNING_LEFT = 2
    JUMPING = 3


class Player(Entity):
    def __init__(self, x, y, width, height):
        player_sprite_path = Path(__file__).parent.parent.parent / 'assets' / 'player' / 'standing.png'
        super().__init__(x, y, width, height, player_sprite_path)
        self.sprite = pygame.image.load(player_sprite_path)
        self.sprite = pygame.transform.scale(self.sprite, (width, height))
        self.state = States.STANDING

        self.current_running_frame = 0
        self.running_frames = []
        for i in range(27):
            frame_path = Path(__file__).parent.parent.parent / 'assets' / 'player' / 'running' / f"{i + 1}.png"
            frame = pygame.image.load(frame_path)
            frame = pygame.transform.scale(frame, (width, height))
            self.running_frames.append(frame)

        # TODO: self.jumping_frames ...

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

    def move_left(self):
        self.move(Vector(-self.movement_speed, 0))

    def move_right(self):
        self.move(Vector(self.movement_speed, 0))

    def _update_running_frame(self):
        self.current_running_frame += 1
        if self.current_running_frame == 27:  # для того чтобы слишком быстро не бежал
            self.current_running_frame = 0

