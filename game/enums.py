from enum import Enum, auto


class MapData(Enum):
    SPAWN_POSITION = auto()
    BLOCKS = auto()
    TILE_SIZE = auto()


class GameObjectData(Enum):
    X = auto()
    Y = auto()
    WIDTH = auto()
    HEIGHT = auto()
    SPRITE_PATH = auto()


class PlayerStates(Enum):
    STANDING = auto()
    RUNNING_RIGHT = auto()
    RUNNING_LEFT = auto()
    JUMPING = auto()
