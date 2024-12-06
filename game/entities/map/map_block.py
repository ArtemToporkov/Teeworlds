from os.path import join

from game.entities.game_object import GameObject
import pygame as pg

from game.constants import ASSETS_PATH


class MapBlock(GameObject):
    def __init__(self, x, y, width, height, sprite_path=None):
        super().__init__(x, y, width, height)
        self.sprite_path = sprite_path
        self.sprite = None
        if sprite_path is not None:
            self.sprite = pg.image.load(sprite_path).convert_alpha()
            self.sprite = pg.transform.scale(self.sprite, (width, height))

    def draw(self, screen, center):
        if self.sprite is None:
            super().draw(screen, center)
            return
        _, top_left, _ = self.convert_coordinates(center)
        screen.blit(self.sprite, (top_left.x, top_left.y, self.width, self.height))

    def to_dict(self):
        data = super().to_dict()
        data["sprite_path"] = self.sprite_path
        return data

    @staticmethod
    def from_dict(data):
        block = super(MapBlock, MapBlock).from_dict(data)
        block.sprite_path = data.get("sprite_path")
        return block
