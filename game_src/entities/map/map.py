import pygame

from game_src.entities.game_object import GameObject
from game_src.entities.map.platform import Platform
import pygame as pg

from game_src.utils.enums import MapData
from geometry.vector import Vector
from game_src.constants import ASSETS_PATH, WINDOW_WIDTH, WINDOW_HEIGHT, MAP_WIDTH, MAP_HEIGHT
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

    def draw_boundary(self, screen, offset_x, offset_y):
        # Настройки цвета и параметров
        border_color = (255, 0, 0)  # Красный цвет
        background_color = (100, 0, 0)  # Темный оттенок красного
        line_thickness = 4
        dash_length = 15
        corner_radius = 20  # Радиус скругленных углов

        # Определение границ карты с учетом смещения
        left = offset_x
        top = offset_y
        right = MAP_WIDTH + offset_x
        bottom = MAP_HEIGHT + offset_y

        # Функция для рисования пунктирной линии
        def draw_dashed_line(start, end, fixed, is_horizontal):
            current = start
            while current < end:
                dash_end = min(current + dash_length, end)
                if is_horizontal:
                    pygame.draw.line(screen, border_color, (current, fixed), (dash_end, fixed), line_thickness)
                else:
                    pygame.draw.line(screen, border_color, (fixed, current), (fixed, dash_end), line_thickness)
                current += 2 * dash_length  # Пропуск между штрихами

        # Рисуем закругленные углы
        pygame.draw.arc(screen, border_color, (left, top, corner_radius * 2, corner_radius * 2), 3.14, 4.71,
                        line_thickness)
        pygame.draw.arc(screen, border_color, (right - corner_radius * 2, top, corner_radius * 2, corner_radius * 2),
                        4.71, 6.28, line_thickness)
        pygame.draw.arc(screen, border_color, (left, bottom - corner_radius * 2, corner_radius * 2, corner_radius * 2),
                        1.57, 3.14, line_thickness)
        pygame.draw.arc(screen, border_color,
                        (right - corner_radius * 2, bottom - corner_radius * 2, corner_radius * 2, corner_radius * 2),
                        0, 1.57, line_thickness)

        # Рисуем пунктирные линии между углами
        draw_dashed_line(left + corner_radius, right - corner_radius, top, is_horizontal=True)  # Верхняя
        draw_dashed_line(left + corner_radius, right - corner_radius, bottom, is_horizontal=True)  # Нижняя
        draw_dashed_line(top + corner_radius, bottom - corner_radius, left, is_horizontal=False)  # Левая
        draw_dashed_line(top + corner_radius, bottom - corner_radius, right, is_horizontal=False)  # Правая

    def draw(self, screen: pygame.display, center: GameObject) -> None:
        # Расчет смещения камеры
        camera_x = max(WINDOW_WIDTH / 2, min(center.position.x, MAP_WIDTH - WINDOW_WIDTH / 2))
        camera_y = max(WINDOW_HEIGHT / 2, min(center.position.y, MAP_HEIGHT - WINDOW_HEIGHT / 2))

        # Расчет смещения камеры
        offset_x = -camera_x + WINDOW_WIDTH / 2
        offset_y = -camera_y + WINDOW_HEIGHT / 2

        # Масштабируем фон под размеры карты
        scaled_background = pg.transform.scale(self.image, (MAP_WIDTH, MAP_HEIGHT))

        # Отрисовка фона с учетом смещения
        screen.blit(scaled_background, (offset_x, offset_y))

        # Отрисовка платформ (или других объектов)
        for block in self.platforms:
            block.draw(screen, center)

