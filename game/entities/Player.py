import pygame

from game.entities.Entity import Entity
from geometry.Vector import Vector


class Player(Entity):
    def __init__(self, x, y, width, height, sprite_path):
        super().__init__(x, y, width, height, sprite_path)
        self.sprite = pygame.image.load(sprite_path)

    def draw(self, screen: pygame.display):
        screen.blit(self.sprite, (self.position.x, self.position.y))

    def move_left(self):
        self.move(Vector(-self.movement_speed, 0))

    def move_right(self):
        self.move(Vector(self.movement_speed, 0))

