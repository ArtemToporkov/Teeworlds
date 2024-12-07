import pygame

from game.entities.map.platform import Platform
import pygame as pg

from game.enums import MapData
from geometry.Vector import Vector
from game.constants import ASSETS_PATH
from os.path import join
from typing import Type
from pathlib import Path


class Map:
    def __init__(self):
        self.blocks = {(200, 200): Platform(
            50, 200, 200, 200, Path(__file__).parent.parent.parent.parent / 'assets' / 'platforms' / '1.png')}
        self.tile_size = 50
        self.spawn_position = Vector(0, 0)
        self.image = pg.image.load(join(ASSETS_PATH, "maps", "background.png"))
        self.image.set_alpha(128)
        self.image = pg.transform.scale(self.image, (800, 600))

    @classmethod
    def from_dict(cls: Type['Map'], data: dict) -> 'Map':
        new_map = cls()
        new_map.spawn_position = Vector(*data[MapData.SPAWN_POSITION])
        new_map.tile_size = data[MapData.TILE_SIZE]
        new_map.blocks = {
            tuple(map(float, pos)): Platform.from_dict(block_data)
            for pos, block_data in data[MapData.BLOCKS].items()
        }
        return new_map

    @classmethod
    def load_from_file(cls: Type['Map'], filepath: str) -> 'Map':
        import json
        with open(filepath, "r") as f:
            data = json.load(f)
        return cls.from_dict(data)

    def to_dict(self) -> dict[MapData, tuple | dict | int]:
        return {
            MapData.SPAWN_POSITION: self.spawn_position.to_tuple(),
            MapData.BLOCKS: {pos: block.to_dict() for pos, block in self.blocks.items()},
            MapData.TILE_SIZE: self.tile_size,
        }

    def draw(self, screen: pygame.display, center: Vector) -> None:
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

