import ctypes
import sys
from os import environ

import PyQt5
import pygame
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
from pathlib import Path

from game_src.constants import WINDOW_WIDTH, WINDOW_HEIGHT
from src import background


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        ui = Path("MainMenu.ui")
        loadUi(ui, self)
        self.startButton.clicked.connect(self._start_game)
        self.editorButton.clicked.connect(self._editor)
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
        from game_src.constants import WINDOW_WIDTH, WINDOW_HEIGHT

        self.hide()
        QApplication.exit(0)
        # self.close()

        from game_src.game import Game

        from pygame import display
        print(f'width: {WINDOW_WIDTH}, height: {WINDOW_HEIGHT}')
        screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        print(display.get_window_size())
        game = Game(screen)

        game.run()

    def _editor(self) -> None:
        from levels_editor.editor import Editor
        self.close()
        editor = Editor()
        editor.show()


def main():
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    # window.setFixedSize(1920, 1080)
    # window.resize(1920, 1080)
    # window.update()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
