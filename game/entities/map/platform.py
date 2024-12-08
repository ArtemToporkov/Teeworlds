import os
import pygame
from pygame import Vector2

from game.constants import MOVEMENT_SPEED, WINDOW_WIDTH, WINDOW_HEIGHT
from game.entities.game_object import GameObject
from game.entities.player import Player
from geometry.Vector import Vector
from game.enums import Collisions


class Platform(GameObject):
    def __init__(self, x, y, width, height, sprite_path: os.path = None):
        super().__init__(x, y, width, height, sprite_path)
        self.sprite = pygame.image.load(sprite_path)
        self.sprite = pygame.transform.scale(self.sprite, (width, height))

    def draw(self, screen, center):
        new_position = self.get_coordinates_offset_by_center(center)
        screen.blit(self.sprite, (new_position.x, new_position.y, self.width, self.height))

    def get_collisions(self, other: GameObject) -> dict[Collisions, bool]:
        object_to_check_clone = GameObject(
            x=other.position.x, y=other.position.y, width=other.width, height=other.height,
        )
        delta = MOVEMENT_SPEED
        return {
            Collisions.X_RIGHT: self._move_and_check_collisions(object_to_check_clone, delta, 0),
            Collisions.X_LEFT: self._move_and_check_collisions(object_to_check_clone, -delta, 0),
            Collisions.Y_UP: self._move_and_check_collisions(object_to_check_clone, 0, -delta),
            Collisions.Y_DOWN: self._move_and_check_collisions(object_to_check_clone, 0, delta)
        }

    def _move_and_check_collisions(self, fake: GameObject, dx, dy) -> bool:
        fake.position.x, fake.position.y = fake.position.x + dx, fake.position.y + dy
        result = self.intersects(fake)
        fake.position.x, fake.position.y = fake.position.x - dx, fake.position.y - dy
        return result



