import os
import pygame
from game.entities.game_object import GameObject


class Platform(GameObject):
    def __init__(self, x, y, width, height, sprite_path: os.path = None):
        super().__init__(x, y, width, height, sprite_path)
        self.sprite = pygame.image.load(sprite_path)
        self.sprite = pygame.transform.scale(self.sprite, (width, height))

    def draw(self, screen, center):
        new_position = self.get_coordinates_offset_by_center(center)
        screen.blit(self.sprite, (new_position.x, new_position.y, self.width, self.height))
