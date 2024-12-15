import os
import unittest
from unittest.mock import Mock, patch
from game_src.utils.enums import GameObjectData, Collisions
from geometry.vector import Vector
from game_src.constants import WINDOW_HEIGHT, WINDOW_WIDTH, ASSETS_PATH
from game_src.entities.game_object import GameObject


class TestGameObject(unittest.TestCase):
    def setUp(self):
        # Создаем тестовый объект
        self.obj = GameObject(x=10, y=20, width=50, height=60, sprite_path=os.path.join(ASSETS_PATH, 'maps', 'background.png'))

    def test_initialization(self):
        self.assertEqual(self.obj.position, Vector(10, 20))
        self.assertEqual(self.obj.size, Vector(50, 60))
        self.assertTrue(self.obj.alive)
        self.assertEqual(self.obj.velocity, Vector(0, 0))

    def test_to_dict(self):
        with patch('game_src.utils.serialization_tools.packing_path', return_value="test_path"):
            data = self.obj.to_dict()
            self.assertEqual(data[GameObjectData.POSITION_X.value], 10)
            self.assertEqual(data[GameObjectData.POSITION_Y.value], 20)
            self.assertEqual(data[GameObjectData.WIDTH.value], 50)
            self.assertEqual(data[GameObjectData.HEIGHT.value], 60)

    def test_from_dict(self):
        data = {
            GameObjectData.POSITION_X.value: 15,
            GameObjectData.POSITION_Y.value: 25,
            GameObjectData.WIDTH.value: 100,
            GameObjectData.HEIGHT.value: 200,
            GameObjectData.VELOCITY.value: (1, 1),
            GameObjectData.DIRECTION.value: (0, 1),
            GameObjectData.SPRITE_PATH.value: os.path.join(ASSETS_PATH, 'maps', 'background.png'),
        }
        obj = GameObject.from_dict(data)
        self.assertEqual(obj.position, Vector(15, 25))
        self.assertEqual(obj.size, Vector(100, 200))
        self.assertEqual(obj.velocity, Vector(1, 1))

    def test_intersects(self):
        other = GameObject(x=50, y=50, width=30, height=30)
        self.assertTrue(self.obj.intersects(other))  # Не пересекаются

        other.position = Vector(30, 30)
        self.assertTrue(self.obj.intersects(other))  # Пересекаются

    def test_move(self):
        self.obj.move(Vector(10, 5))
        self.assertEqual(self.obj.position, Vector(20, 25))

    def test_update_velocity_limit(self):
        self.obj.velocity = Vector(100, 0)  # Скорость больше 25
        self.obj.update()
        self.assertAlmostEqual(self.obj.velocity.length(), 25)

    @patch('pygame.Surface')
    def test_draw(self, mock_surface):
        mock_screen = Mock()
        center_obj = GameObject(x=5, y=5, width=20, height=20)
        self.obj.draw(mock_screen, center_obj)
        self.assertTrue(mock_screen.blit.called)

    @patch('pygame.draw.circle')
    @patch('pygame.draw.rect')
    def test_draw_hitbox(self, mock_draw_rect, mock_draw_circle):
        mock_screen = Mock()
        center_obj = GameObject(x=5, y=5, width=20, height=20)
        self.obj.draw_hitbox(mock_screen, center_obj)
        self.assertTrue(mock_draw_circle.called)
        self.assertTrue(mock_draw_rect.called)


if __name__ == "__main__":
    unittest.main()
