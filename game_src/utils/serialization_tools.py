import importlib

from game_src.entities.game_object import GameObject
from game_src.entities.guns.bullets import Bullet, BlowingBullet
from game_src.entities.player import Player
from game_src.utils.enums import TypeData


CLASS_MAP = {
    "Player": Player,
    "Bullet": Bullet,
    "BlowingBullet": BlowingBullet,
    "GameObject": GameObject
}

def get_entity(data):
    cls = get_entity_type(data)

    # Проверяем, есть ли метод from_dict
    if hasattr(cls, "from_dict"):
        return cls.from_dict(data)
    else:
        raise ValueError(f"Class '{cls.__class__.__name__}' does not implement 'from_dict' method")

def get_entity_type(data):
    class_name = data.get(TypeData.TYPE.value)
    if not class_name:
        raise ValueError("Field 'type' is missing in the data")

    cls = CLASS_MAP.get(class_name)
    if not cls:
        raise ValueError(f"Unknown class name '{class_name}'")
    return cls
