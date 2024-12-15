import unittest
from unittest.mock import MagicMock, patch

from game_src.constants import ASSETS_PATH
from game_src.entities.guns.bullets import Bullet, BlowingBullet
from game_src.entities.guns.weapons import Weapon, Pistol, ShotGun, Rocket, MedKit
from geometry.vector import Vector
import os
import pygame as pg


class TestWeaponModule(unittest.TestCase):
    @patch("pygame.image.load")
    @patch("pygame.transform.scale")
    def test_image_loader_load_sprite(self, mock_scale, mock_load):
        mock_load.return_value.get_height.return_value = 100
        mock_load.return_value.get_width.return_value = 200
        sprite_path = "test_path.png"
        width = 50

        result = Weapon(0, 0, width, 50, sprite_path).image

        self.assertIsNotNone(result)
        mock_load.assert_called()
        mock_scale.assert_called()

    def test_weapon_initialization(self):
        weapon = Weapon(0, 0, 50, 50, os.path.join(ASSETS_PATH, "weapons", "pistol.png"))
        self.assertEqual(weapon.kickback, 0)
        self.assertEqual(weapon.direction, Vector(0, 0))
        self.assertEqual(weapon.dist, 30)
        self.assertIsNotNone(weapon.image)

    def test_pistol_get_bullets(self):
        pistol = Pistol(0, 0, 50, 50, os.path.join(ASSETS_PATH, "weapons", "pistol.png"))
        pistol.direction = Vector(1, 0)
        bullets = pistol.get_bullets()

        self.assertEqual(len(bullets), 1)
        bullet = bullets[0]
        self.assertIsInstance(bullet, Bullet)
        self.assertEqual(bullet.velocity, Vector(50, 0))

    def test_shotgun_get_bullets(self):
        shotgun = ShotGun(0, 0, 50, 50, os.path.join(ASSETS_PATH, "weapons", "pistol.png"))
        shotgun.direction = Vector(1, 0)
        bullets = shotgun.get_bullets()

        self.assertEqual(len(bullets), 5)
        for bullet in bullets:
            self.assertIsInstance(bullet, Bullet)

    def test_rocket_get_bullets(self):
        rocket = Rocket(0, 0, 50, 50, os.path.join(ASSETS_PATH, "weapons", "pistol.png"))
        rocket.direction = Vector(0, 1)
        bullets = rocket.get_bullets()

        self.assertEqual(len(bullets), 1)
        bullet = bullets[0]
        self.assertIsInstance(bullet, BlowingBullet)
        self.assertEqual(bullet.velocity, Vector(0, 15))

    def test_medkit_initialization(self):
        medkit = MedKit(0, 0, 50, 50, os.path.join(ASSETS_PATH, "weapons", "pistol.png"), 50)
        self.assertEqual(medkit.hp, 50)

    def test_medkit_get_bullets(self):
        medkit = MedKit(0, 0, 50, 50, os.path.join(ASSETS_PATH, "weapons", "pistol.png"), 50)
        self.assertEqual(medkit.get_bullets(), 50)


if __name__ == "__main__":
    unittest.main()
