import os
from geometry.vector import Vector


def _find_assets_folder():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while current_dir:
        assets_path = os.path.join(current_dir, "assets")
        if os.path.exists(assets_path) and os.path.isdir(assets_path):
            return assets_path
        current_dir = os.path.dirname(current_dir)
    raise FileNotFoundError("Папка 'assets' не найдена.")


DELTA_FOR_COLLISIONS = 2
MAX_HOOK_LENGTH = 400
FPS = 60
MOVEMENT_SPEED = 10
JUMP_STRENGTH = 14

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
BACKGROUND_WIDTH = 1280
BACKGROUND_HEIGHT = 720
MAP_WIDTH = 1800
MAP_HEIGHT = 1300

ASSETS_PATH = _find_assets_folder()
CURRENT_LEVEL = "first level"
GRAVITY = 0.6
HITBOXES_MODE = True
SERVER_ADDR = ("localhost", 8686)
MAX_HP = 100
MAX_DISTANCE_TO_CENTRE_FOR_PLAYER = 2500