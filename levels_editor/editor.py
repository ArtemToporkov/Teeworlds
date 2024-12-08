import sys

import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QWizardPage
from PyQt5.uic import loadUi
from pathlib import Path
from src import platforms


class MainMenu(QWizardPage):
    def __init__(self):
        super().__init__()
        ui = Path("editor.ui")
        loadUi(ui, self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec_())
