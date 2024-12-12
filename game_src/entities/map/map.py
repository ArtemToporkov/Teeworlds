import pygame

from game_src.entities.game_object import GameObject
from game_src.entities.map.platform import Platform
import pygame as pg

from game_src.utils.enums import MapData
from geometry.vector import Vector
from game_src.constants import ASSETS_PATH
from os.path import join
from typing import Type
from pathlib import Path


class Map:
    def __init__(self, platforms: list[Platform], spawn_position: Vector):

        self.platforms = platforms
        self.spawn_position = spawn_position
        self.tile_size = 50
        self.image = pg.image.load(join(ASSETS_PATH, "maps", "background.png"))
        self.image.set_alpha(128)
        self.image = pg.transform.scale(self.image, (800, 600))

    @classmethod
    def from_dict(cls: Type['Map'], data: dict) -> 'Map':
        spawn_position = Vector(*data[MapData.SPAWN_POSITION.value])
        platforms = [Platform.from_dict(platform) for platform in data[MapData.PLATFORMS.value]]
        new_map = cls(platforms, spawn_position)
        return new_map

    @classmethod
    def load_from_file(cls: Type['Map'], filepath: str) -> 'Map':
        import json
        with open(filepath, "r") as f:
            data = json.load(f)
        return cls.from_dict(data)

    def to_dict(self) -> dict[MapData, tuple | dict | int]:
        return {
            MapData.SPAWN_POSITION.value: self.spawn_position.to_tuple(),
            MapData.PLATFORMS.value: [platform.to_dict() for platform in self.platforms],
            MapData.TILE_SIZE.value: self.tile_size,
        }

    def draw(self, screen: pygame.display, center: GameObject) -> None:
        x = (-(center.position // 2) % (self.image.get_width())).x
        y = (-(center.position // 2) % (self.image.get_height())).y
        top_left = Vector(x, y)

        screen.blit(self.image, (top_left.x, top_left.y))
        screen.blit(self.image, (top_left.x - self.image.get_width(), top_left.y))
        screen.blit(self.image, (top_left.x, top_left.y - self.image.get_height()))
        screen.blit(
            self.image,
            (top_left.x - self.image.get_width(), top_left.y - self.image.get_height()),
        )
        for block in self.platforms:
            block.draw(screen, center)

