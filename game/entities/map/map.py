from game.entities.map.map_block import MapBlock
import pygame as pg
from geometry.Vector import Vector
from game.constants import ASSETS_PATH
from os.path import join


class Map:
    def __init__(self):
        self.blocks = dict()
        self.tile_size = 50
        self.spawn_position = Vector(0, 0)
        self.image = pg.image.load(join(ASSETS_PATH, "maps", "background.png"))
        self.image.set_alpha(128)
        self.image = pg.transform.scale(self.image, (800, 600))

    @classmethod
    def from_dict(cls, data):
        new_map = cls()
        new_map.spawn_position = Vector(*data["spawn_position"])
        new_map.tile_size = data["tile_size"]
        new_map.blocks = {
            tuple(map(float, pos)): MapBlock.from_dict(block_data)
            for pos, block_data in data["blocks"].items()
        }
        return new_map

    @classmethod
    def load_from_file(cls, filepath):
        import json

        with open(filepath, "r") as f:
            data = json.load(f)
        return cls.from_dict(data)

    def to_dict(self):
        return {
            "spawn_position": self.spawn_position.to_tuple(),
            "blocks": {pos: block.to_dict() for pos, block in self.blocks.items()},
            "tile_size": self.tile_size,
        }

    def draw(self, screen, center: Vector):
        x = (-(center // 2) % (self.image.get_width())).x
        y = (-(center // 2) % (self.image.get_height())).y
        top_left = Vector(x, y)

        screen.blit(self.image, (top_left.x, top_left.y))
        screen.blit(self.image, (top_left.x - self.image.get_width(), top_left.y))
        screen.blit(self.image, (top_left.x, top_left.y - self.image.get_height()))
        screen.blit(
            self.image,
            (top_left.x - self.image.get_width(), top_left.y - self.image.get_height()),
        )
        for block in self.blocks.values():
            block.draw(screen, center)
