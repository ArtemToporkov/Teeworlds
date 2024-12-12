import sys

import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
from pathlib import Path
from src import background


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        ui = Path("MainMenu.ui")
        loadUi(ui, self)
        self.startButton.clicked.connect(self._start_game)
        self.editorButton.clicked.connect(self._editor)

    def _start_game(self) -> None:
        self.close()

        from game_src.game import Game
        from game_src.constants import WINDOW_WIDTH, WINDOW_HEIGHT
        from pygame import display
        screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
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
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
