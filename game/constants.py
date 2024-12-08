import os
from geometry.Vector import Vector


def _find_assets_folder():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while current_dir:
        assets_path = os.path.join(current_dir, "assets")
        if os.path.exists(assets_path) and os.path.isdir(assets_path):
            return assets_path
        current_dir = os.path.dirname(current_dir)
    raise FileNotFoundError("Папка 'assets' не найдена.")


FPS = 60
MOVEMENT_SPEED = 10
JUMP_STRENGTH = 14
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
BACKGROUND_WIDTH = 1280
BACKGROUND_HEIGHT = 720
ASSETS_PATH = _find_assets_folder()
GRAVITY = Vector(0, 0.6)
GRAVITY_Y = 0.6
HITBOXES_MODE = True
