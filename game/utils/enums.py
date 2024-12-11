from enum import Enum, auto


class MapData(Enum):
    SPAWN_POSITION = auto()
    BLOCKS = auto()
    TILE_SIZE = auto()


class TypeData(Enum):
    TYPE = auto()

class GameObjectData(Enum):
    ID = auto()
    POSITION_X = auto()
    POSITION_Y = auto()
    VELOCITY = auto()
    WIDTH = auto()
    HEIGHT = auto()
    DIRECTION = auto()
    SPRITE_PATH = auto()


class PlayerData(Enum):
    STATE = auto()
    CURRENT_WEAPON = auto()
    HOOK_END = auto()


class BulletData(Enum):
    DAMAGE = auto()


class BlowingBulletData(Enum):
    RADIUS = auto()


class PlayerStates(Enum):
    STANDING = auto()
    RUNNING_RIGHT = auto()
    RUNNING_LEFT = auto()
    JUMPING = auto()


class Collisions(Enum):
    X_RIGHT = auto()
    X_LEFT = auto()
    Y_UP = auto()
    Y_DOWN = auto()
