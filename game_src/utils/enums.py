import enum
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
    HOOK_POSITION = 'hook_position'
    HP = 'hp'
    FORCE_VECTOR = 'force_vector'
    HOOK_VECTOR = 'hook_vector'


class BulletData(Enum):
    DAMAGE = 'damage'
    DIRECTION = 'direction'


class BlowingBulletData(Enum):
    RADIUS = 'radius'


@enum.unique
class PlayerStates(Enum):
    STANDING = auto()
    RUNNING = auto()
    IN_AIR = auto()
    LOOKING_RIGHT = auto()
    LOOKING_LEFT = auto()


class Collisions(Enum):
    X_RIGHT = auto()
    X_LEFT = auto()
    Y_UP = auto()
    Y_DOWN = auto()


def get_state_by_value(value):
    for state in PlayerStates:
        if state.value == value:
            return state
    raise ValueError(f"No state with value {value} found.")
