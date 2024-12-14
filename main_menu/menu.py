import ctypes
import multiprocessing
import os
import sys
from enum import Enum, auto
from os import environ
from pathlib import Path

import PyQt5
import pygame
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
from src import background


class Buttons(Enum):
    START = auto()
    EDITOR = auto()
    EXIT = auto()


class MainMenu(QMainWindow):
    def __init__(self, app: QApplication):
        super().__init__()
        self.button_clicked = None
        ui = Path("MainMenu.ui")
        loadUi(ui, self)
        self._change_multiplayer_mode(0)
        self.startButton.clicked.connect(self._start_game)
        self.editorButton.clicked.connect(self._open_editor)
        self.exitButton.clicked.connect(self.close)
        self.multiplayerCheckBox.stateChanged.connect(self._change_multiplayer_mode)
        if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
            PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
            # enable highdpi scaling

        if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
            PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
            # use highdpi icons

        DS = "1.5"

        scaleFactor = str(ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100)
        if float(scaleFactor) > float(DS):
            scaleFactor = DS

        environ["QT_DEVICE_PIXEL_RATIO"] = "0"
        environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"
        environ["QT_SCALE_FACTOR"] = "1"
        environ["QT_SCREEN_SCALE_FACTORS"] = scaleFactor

    def _start_game(self) -> None:
        self.button_clicked = Buttons.START
        self.close()

    def _open_editor(self) -> None:
        self.button_clicked = Buttons.EDITOR
        self.close()

    def _change_multiplayer_mode(self, state):
        with open(str(Path(__file__).parent.parent / "game_src" / "config.ini"), "w") as f:
            f.write("[Multiplayer]\n")
            f.write(f"MULTIPLAYER = {'True' if state == 2 else 'False'}")


def main():
    app = QApplication(sys.argv)
    window = MainMenu(app)
    window.show()
    exit_code = app.exec_()

    match window.button_clicked:
        case Buttons.START:
            game_process = multiprocessing.Process(target=_run_game)
            game_process.start()
        case Buttons.EDITOR:
            editor_loc = Path(__file__).parent.parent / 'levels_editor'
            os.chdir(editor_loc)  # меняем текущую директорию для корректных импортов
            from levels_editor.editor import main as editor_main
            editor_main()
        case _:
            pass

    sys.exit(exit_code)


def _run_game() -> None:
    from game_src.constants import WINDOW_WIDTH, WINDOW_HEIGHT
    from game_src.game import Game
    from pygame import display
    screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    game = Game(screen)
    game.run()
    pygame.quit()


if __name__ == '__main__':
    main()
