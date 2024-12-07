from geometry.Vector import Vector
import pygame as pg

from game.entities.game_object import GameObject


def load_animation(file_name):
    """ Разрезает спрайт лист на отдельные спрайты, ориентируясь на размер """
    sprite_sheet = pg.image.load(file_name).convert_alpha()

    sprites = []
    for i in range(sprite_sheet.get_width() // sprite_sheet.get_height()):
        surface = pg.Surface((32, 32), pg.SRCALPHA, 32)
        rect = pg.Rect(i * 32, 0, 32, 32)
        surface.blit(sprite_sheet, (0, 0), rect)
        sprites.append(surface)
    return sprites


class Effect(GameObject):
    def __init__(self, x, y, width, height, animation_path=None, lifetime=120):
        super().__init__(x, y, width, height)
        self.velocity = Vector(0, 0)
        self.image = pg.Surface((width, height))
        if animation_path is not None:
            self.animation = [
                pg.transform.scale(animation, (self.width, self.height))
                for animation in load_animation(animation_path)
            ]
        self.lifetime = lifetime
        self.alive = True

    def update(self):
        self.position += self.velocity
        self.animate()
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.alive = False

    def animate(self):
        self.frames += 0.2
        if self.frames >= len(self.animation):
            self.alive = False
            self.frames = 0
        self.image = self.animation[int(self.frames)]

    def draw(self, screen, center):
        position, _, _ = self.convert_coordinates(center)
        rect = self.image.get_rect(center=position.tuple)
        screen.blit(self.image, rect)