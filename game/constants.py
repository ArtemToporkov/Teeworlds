import os


def _find_assets_folder():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while current_dir:
        assets_path = os.path.join(current_dir, "assets")
        if os.path.exists(assets_path) and os.path.isdir(assets_path):
            return assets_path
        current_dir = os.path.dirname(current_dir)
    raise FileNotFoundError("Папка 'assets' не найдена.")


FPS = 60
MOVEMENT_SPEED = 7
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
BACKGROUND_WIDTH = 1280
BACKGROUND_HEIGHT = 720
ASSETS_PATH = _find_assets_folder()
