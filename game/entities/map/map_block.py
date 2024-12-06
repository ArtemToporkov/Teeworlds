import os
import pygame
from game.entities.game_object import GameObject


class Platform(GameObject):
    def __init__(self, x, y, width, height, sprite_path: os.path = None):
        super().__init__(x, y, width, height, sprite_path)
        self.sprite = pygame.image.load(sprite_path)
        self.sprite = pygame.transform.scale(self.sprite, (width, height))

    def draw(self, screen):
        screen.blit(self.sprite, (self.position.x, self.position.y, self.width, self.height))

    def to_dict(self):
        data = super().to_dict()
        data["sprite_path"] = self.sprite_path
        return data

    @staticmethod
    def from_dict(data):
        block = super(Platform, Platform).from_dict(data)
        block.sprite_path = data.get("sprite_path")
        return block
