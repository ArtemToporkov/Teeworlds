import os.path
import unittest
from unittest.mock import patch, Mock, MagicMock

from game_src.constants import ASSETS_PATH
from game_src.entities.game_object import GameObject
from geometry.vector import Vector
from game_src.entities.map.platform import Platform
from game_src.entities.map.map import Map
from game_src.utils.enums import MapData, Collisions
import pygame


class TestMap(unittest.TestCase):
    def setUp(self):
        self.platforms = [
            Platform(0, 0, 50, 50, sprite_path=os.path.join(ASSETS_PATH, 'platforms', '1.png')),
            Platform(50, 50, 100, 100, sprite_path=os.path.join(ASSETS_PATH, 'platforms', '2.png')),
        ]
        self.spawn_position = Vector(10, 20)
        self.map_instance = Map(self.platforms, self.spawn_position)

    @patch("pygame.image.load")
    def test_init_map(self, mock_load):
        mock_load.return_value = Mock()
        new_map = Map(self.platforms, self.spawn_position)
        self.assertEqual(new_map.spawn_position, self.spawn_position)
        self.assertEqual(new_map.platforms, self.platforms)

    def test_to_dict(self):
        expected_dict = {
            MapData.SPAWN_POSITION.value: (10, 20),
            MapData.PLATFORMS.value: [platform.to_dict() for platform in self.platforms],
            MapData.TILE_SIZE.value: 50,
        }
        self.assertEqual(self.map_instance.to_dict(), expected_dict)

    def test_from_dict(self):
        data = {
            MapData.SPAWN_POSITION.value: (10, 20),
            MapData.PLATFORMS.value: [platform.to_dict() for platform in self.platforms],
        }
        loaded_map = Map.from_dict(data)
        self.assertEqual(loaded_map.spawn_position, self.spawn_position)
        self.assertEqual(len(loaded_map.platforms), len(self.platforms))

    @patch("pygame.display.set_mode")
    @patch("pygame.image.load")
    def test_draw(self, mock_image_load, mock_set_mode):
        screen = mock_set_mode.return_value
        mock_image_load.return_value = MagicMock()
        mock_center = GameObject(1, 2, 2, 3,)
        self.map_instance.draw(screen, mock_center)
        screen.blit.assert_called()


class TestPlatform(unittest.TestCase):
    def setUp(self):
        self.platform = Platform(0, 0, 50, 50, sprite_path=os.path.join(ASSETS_PATH, 'platforms', '1.png'))
        self.other = Platform(10, 10, 30, 30, sprite_path=os.path.join(ASSETS_PATH, 'platforms', '1.png'))

    @patch("pygame.image.load")
    @patch("pygame.transform.scale")
    def test_init_platform(self, mock_scale, mock_load):
        mock_load.return_value = Mock()
        mock_scale.return_value = Mock()
        new_platform = Platform(10, 20, 30, 40, sprite_path=os.path.join(ASSETS_PATH, 'platforms', '1.png'))
        self.assertEqual(new_platform.width, 30)
        self.assertEqual(new_platform.height, 40)

    @patch("pygame.display.set_mode")
    def test_draw(self, mock_set_mode):
        screen = mock_set_mode.return_value
        center = GameObject(1, 2, 2, 3,)
        self.platform.draw(screen, center)
        screen.blit.assert_called()

    def test_to_dict(self):
        data = self.platform.to_dict()
        self.assertEqual(data["pos_x"], 0)
        self.assertEqual(data["pos_y"], 0)
        self.assertEqual(data["width"], 50)
        self.assertEqual(data["height"], 50)

    def test_get_collisions(self):
        move_vector = Vector(5, 5)
        collisions = self.platform.get_collisions(self.other, move_vector)
        self.assertIn(Collisions.X_RIGHT, collisions)
        self.assertIn(Collisions.X_LEFT, collisions)

    def test_from_dict(self):
        data = {
            "pos_x": 10,
            "pos_y": 20,
            "width": 30,
            "height": 40,
            "sprite_path": os.path.join(ASSETS_PATH, 'platforms', '1.png'),
        }
        platform = Platform.from_dict(data)
        self.assertEqual(platform.width, 30)
        self.assertEqual(platform.height, 40)


if __name__ == "__main__":
    unittest.main()
