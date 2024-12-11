import os
import pygame

from game.entities.game_object import GameObject
from geometry.vector import Vector
from game.utils.enums import Collisions


class Platform(GameObject):
    def __init__(self, x, y, width, height, sprite_path: os.path = None):
        super().__init__(x, y, width, height, sprite_path)
        self.sprite = pygame.image.load(sprite_path)
        self.sprite = pygame.transform.scale(self.sprite, (width, height))

    def draw(self, screen, center):
        new_position = self.get_coordinates_offset_by_center(center)
        screen.blit(self.sprite, (new_position.x, new_position.y, self.width, self.height))

    def get_collisions(self, other: GameObject, potential_move: Vector) -> dict[Collisions, bool]:
        object_to_check_clone = GameObject(
            x=other.position.x, y=other.position.y, width=other.width, height=other.height,
        )
        dx, dy = abs(potential_move.x), abs(potential_move.y)
        return {
            Collisions.X_RIGHT: self._move_and_check_collisions(object_to_check_clone, dx, 0),
            Collisions.X_LEFT: self._move_and_check_collisions(object_to_check_clone, -dx, 0),
            Collisions.Y_UP: self._move_and_check_collisions(object_to_check_clone, 0, -dy),
            Collisions.Y_DOWN: self._move_and_check_collisions(object_to_check_clone, 0, dy)
        }

    def _move_and_check_collisions(self, fake: GameObject, dx, dy) -> bool:
        fake.position.x, fake.position.y = fake.position.x + dx, fake.position.y + dy
        result = self.intersects(fake)
        fake.position.x, fake.position.y = fake.position.x - dx, fake.position.y - dy
        return result



