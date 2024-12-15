import pytest
from unittest.mock import Mock, patch

from game_src.entities.game_object import GameObject
from game_src.entities.player import Player
from geometry.vector import Vector
from game_src.constants import MAX_HP, MOVEMENT_SPEED
import pygame as pg


@pytest.fixture
def player():
    """Создает экземпляр Player для тестов."""
    return Player(x=100, y=200, width=50, height=50)


def test_initialization(player):
    """Тест инициализации объекта Player."""
    assert player.position == Vector(100, 200)
    assert player.hp == MAX_HP
    assert player.alive is True
    assert len(player.weapons) > 0
    assert player.current_weapon == 0


@patch('pygame.draw.rect')
@patch("pygame.image.load")
def test_draw(mock_load, _ ,player):
    """Тест отрисовки игрока."""
    mock_screen = Mock()
    center = GameObject(1, 1, 1, 1)
    player.draw(mock_screen, center)
    mock_load.assert_not_called()


def test_update(player):
    """Тест обновления состояния игрока."""
    player.hp -= 20
    player.update()
    assert player.hp == MAX_HP if not player.alive else MAX_HP - 20

    player.position = Vector(-10, 0)
    player.update()
    assert player.alive is False


def test_interact_with_bullet(player):
    """Тест взаимодействия с пулей."""
    mock_bullet = Mock()
    mock_bullet.damage = 20
    mock_bullet.alive = True
    mock_bullet.position = player.position
    mock_bullet.width = 10
    mock_bullet.height = 10

    player.interact(mock_bullet)
    assert player.hp == 100
    assert mock_bullet.alive is True
