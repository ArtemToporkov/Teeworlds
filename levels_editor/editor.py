import sys
import time
from functools import partial

import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QWizardPage
from PyQt5.uic import loadUi
from pathlib import Path
from levels_editor.src import src


class Editor(QWizardPage):
    def __init__(self):
        super().__init__()
        ui = Path(__file__).parent / 'editor.ui'
        loadUi(ui, self)
        self._connect_platforms_and_spawn_buttons()
        self.exitButton.clicked.connect(lambda _: self.close())
        self.current_selected_item = None

    def _connect_platforms_and_spawn_buttons(self):
        for platform in [
            self.firstPlatform, self.secondPlatform, self.thirdPlatform, self.fourthPlatform, self.fifthPlatform,
            self.sixthPlatform, self.seventhPlatform, self.spawnButton
        ]:
            platform.clicked.connect(partial(self._on_platform_clicked, platform))

    @staticmethod
    def _on_platform_clicked(*args):
        platform = args[0]
        print(platform.objectName())


def main():
    app = QApplication(sys.argv)
    window = Editor()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
