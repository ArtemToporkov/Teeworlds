import unittest
from unittest.mock import MagicMock, patch
import pygame
from pathlib import Path
from game_src.entities.game_object import GameObject
from game_src.entities.guns.bullets import Bullet
from game_src.entities.guns.weapons import Pistol, ShotGun, Rocket, MedKit
from game_src.utils.enums import PlayerStates, Collisions, PlayerData, GameObjectData, TypeData
from geometry.vector import Vector
from game_src.entities.player import Player


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player(x=100, y=100, width=50, height=50)

    def test_initialization(self):
        self.assertEqual(self.player.position.x, 100)
        self.assertEqual(self.player.position.y, 100)
        self.assertEqual(self.player.width, 50)
        self.assertEqual(self.player.height, 50)
        self.assertEqual(self.player.state, PlayerStates.STANDING)
        self.assertEqual(self.player.hp, 100)
        self.assertEqual(self.player.alive, True)
        self.assertEqual(len(self.player.weapons), 4)
        self.assertIsInstance(self.player.weapons[0], Pistol)
        self.assertIsInstance(self.player.weapons[1], ShotGun)
        self.assertIsInstance(self.player.weapons[2], Rocket)
        self.assertIsInstance(self.player.weapons[3], MedKit)

    def test_update(self):
        self.player.hp = 0
        self.player.update()
        self.assertEqual(self.player.alive, False)
        self.assertEqual(self.player.hp, 100)

    def test_interact_with_player(self):
        other_player = Player(x=150, y=150, width=50, height=50)
        self.player.interact(other_player)
        self.assertNotEqual(self.player.velocity, Vector(0, 0))

    def test_interact_with_bullet(self):
        bullet = Bullet(100, 100, 10, 10, 10)
        bullet.damage = 10
        bullet.alive = True
        self.player.interact(bullet)
        self.assertEqual(self.player.hp, 90)
        self.assertFalse(bullet.alive)

    def test_shoot(self):
        self.player.cooldown = -1
        bullets = self.player.shoot()
        self.assertEqual(len(bullets), 1)
        self.assertEqual(self.player.cooldown, 30)

    def test_to_dict(self):
        data = self.player.to_dict()
        self.assertEqual(data[TypeData.TYPE.value], 'Player')
        self.assertEqual(data[PlayerData.STATE.value], PlayerStates.STANDING.value)
        self.assertEqual(data[PlayerData.CURRENT_WEAPON.value], 0)
        self.assertEqual(data[PlayerData.HP.value], 100)
        self.assertEqual(data[PlayerData.FORCE_VECTOR.value], (0, 0))

    def test_from_dict(self):
        data = {
            GameObjectData.POSITION_X.value: 100,
            GameObjectData.POSITION_Y.value: 100,
            GameObjectData.WIDTH.value: 50,
            GameObjectData.HEIGHT.value: 50,
            GameObjectData.VELOCITY.value: (0, 0),
            GameObjectData.DIRECTION.value: (0, 0),
            PlayerData.STATE.value: PlayerStates.STANDING.value,
            PlayerData.CURRENT_WEAPON.value: 0,
            PlayerData.HP.value: 100,
            PlayerData.FORCE_VECTOR.value: (0, 0)
        }
        player = Player.from_dict(data)
        self.assertEqual(player.position.x, 100)
        self.assertEqual(player.position.y, 100)
        self.assertEqual(player.width, 50)
        self.assertEqual(player.height, 50)
        self.assertEqual(player.state, PlayerStates.STANDING)
        self.assertEqual(player.hp, 100)
        self.assertEqual(player.current_weapon, 0)
        self.assertEqual(player.move_force_vector, Vector(0, 0))


if __name__ == '__main__':
    unittest.main()
