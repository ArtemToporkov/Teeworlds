import os
import unittest
from unittest.mock import Mock, patch

from game_src.entities.game_object import GameObject
from game_src.entities.guns.bullets import Bullet, BlowingBullet
from game_src.entities.guns.weapons import BULLETS_PATH
from geometry.vector import Vector
from game_src.constants import GRAVITY, ASSETS_PATH


class TestBullet(unittest.TestCase):

    def setUp(self):
        self.bullet = Bullet(0, 0, 10, 10, 50, os.path.join(BULLETS_PATH, "bullet.png"))
        self.bullet.velocity = Vector(5, 5)

    def test_update(self):
        self.bullet.update()
        self.assertEqual(self.bullet.lifetime, 1)
        self.assertTrue(self.bullet.alive)

    def test_lifetime_exceeded(self):
        self.bullet.lifetime = 300
        self.bullet.update()
        self.assertFalse(self.bullet.alive)

    def test_interact_with_player(self):
        mock_player = Mock()
        mock_player.intersects.return_value = True
        self.bullet.interact(mock_player)
        self.assertTrue(self.bullet.alive)

    def test_interact_with_platform(self):
        mock_platform = Mock()
        mock_platform.intersects.return_value = True
        self.bullet.interact(mock_platform)
        self.assertTrue(self.bullet.alive)

    def test_to_dict(self):
        data = self.bullet.to_dict()
        self.assertEqual(data['damage'], 50)
        self.assertEqual(data['direction'], self.bullet.direction.to_tuple())

    def test_from_dict(self):
        data = {
            'pos_x': 0,
            'pos_y': 0,
            'width': 10,
            'height': 10,
            'sprite_path': BULLETS_PATH + '\\' + 'bullet.png',
            'damage': 50,
            'velocity': (5, 5),
            'direction': (1, 0)
        }
        bullet = Bullet.from_dict(data)
        self.assertEqual(bullet.damage, 50)
        self.assertEqual(bullet.direction, Vector(1, 0))


class TestBlowingBullet(unittest.TestCase):

    def setUp(self):
        self.bullet = BlowingBullet(0, 0, 10, 10, 100, os.path.join(BULLETS_PATH, "bullet.png"))
        self.bullet.velocity = Vector(5, 5)

    def test_update(self):
        self.bullet.update()
        self.assertEqual(self.bullet.lifetime, 1)
        self.assertTrue(self.bullet.alive)

    def test_apply_forces(self):
        initial_velocity = self.bullet.velocity.y
        self.bullet.apply_forces()
        self.assertGreater(self.bullet.velocity.y, initial_velocity)

    def test_interact_triggers_blowing(self):
        mock_platform = Mock()
        mock_platform.intersects.return_value = True
        self.bullet.interact(mock_platform)
        self.assertFalse(self.bullet.blowing)

    def test_to_dict(self):
        data = self.bullet.to_dict()
        self.assertEqual(data['damage'], 100)
        self.assertEqual(data['radius'], 150)

    def test_draw(self):
        mock_screen = Mock()
        center = GameObject(1, 2, 2, 3,)
        self.bullet.draw(mock_screen, center)
        self.assertTrue(self.bullet.alive)
