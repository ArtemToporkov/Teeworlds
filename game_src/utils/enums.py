from enum import Enum, auto


class MapData(Enum):
    SPAWN_POSITION = 'spawn_position'
    PLATFORMS = 'platforms'
    TILE_SIZE = 'tile_size'


class TypeData(Enum):
    TYPE = 'type_entity'


class GameObjectData(Enum):
    ID = 'id'
    POSITION_X = 'pos_x'
    POSITION_Y = 'pos_y'
    VELOCITY = 'velocity'
    WIDTH = 'width'
    HEIGHT = 'height'
    DIRECTION = 'direction'
    SPRITE_PATH = 'sprite_path'


class PlayerData(Enum):
    STATE = 'state'
    CURRENT_WEAPON = 'current_weapon'
    HOOK_END = 'hook_end'


class BulletData(Enum):
    DAMAGE = 'damage'
    DIRECTION = 'direction'


class BlowingBulletData(Enum):
    RADIUS = 'radius'


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
