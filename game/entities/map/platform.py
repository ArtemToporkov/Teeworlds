import os
import pygame
from pygame import Vector2

from game.constants import MOVEMENT_SPEED, WINDOW_WIDTH, WINDOW_HEIGHT
from game.entities.game_object import GameObject
from game.entities.player import Player
from geometry.Vector import Vector


class Platform(GameObject):
    def __init__(self, x, y, width, height, sprite_path: os.path = None):
        super().__init__(x, y, width, height, sprite_path)
        self.sprite = pygame.image.load(sprite_path)
        self.sprite = pygame.transform.scale(self.sprite, (width, height))

    def draw(self, screen, center):
        new_position = self.get_coordinates_offset_by_center(center)
        screen.blit(self.sprite, (new_position.x, new_position.y, self.width, self.height))

    def interact(self, other: GameObject):
        if not self.intersects(other):
            return
        if isinstance(other, Player):
            other.move_force_vector = Vector(0, 0)
            self._move_player_beyond_borders(other)

    def _move_player_beyond_borders(self, player: Player):
        # мега костылище
        delta = 1
        player.jumped = False
        player.move_by_coordinates(delta, 0)
        if self.intersects(player):
            player.move_by_coordinates(-delta, 0)
            player.move_by_coordinates(-delta, 0)
        if self.intersects(player):
            player.move_by_coordinates(delta, 0)
            player.move_by_coordinates(0, delta)
        if self.intersects(player):
            player.move_by_coordinates(0, -delta)
            player.move_by_coordinates(0, -delta)



