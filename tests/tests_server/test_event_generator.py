import unittest
from unittest.mock import MagicMock, patch
from game_src.entities.guns.bullets import BlowingBullet
from geometry.vector import Vector
from web.server_src.event_generator import EventGenerator
from web.server_src.server import Server
import asyncio


class TestEventGenerator(unittest.TestCase):
    def setUp(self):
        # Подготовка данных для теста EventGenerator
        self.entities_to_send = {"group1": []}
        self.event_generator = EventGenerator(self.entities_to_send)

    @patch("random.randint", side_effect=[0, 100, 50, 150, 0, 5])
    @patch("time.sleep")
    def test_start_event(self, mock_sleep, mock_randint):
        # Переопределяем методы, чтобы избежать реальных задержек и случайностей
        self.event_generator.running = False  # Завершаем цикл после одного выполнения
        self.event_generator.enabled = True

        with patch("game_src.entities.guns.bullets.BlowingBullet") as mock_bullet:
            mock_bullet_instance = MagicMock()
            mock_bullet.return_value = mock_bullet_instance

            self.event_generator.start_event()

            mock_bullet_instance.to_dict.assert_not_called()