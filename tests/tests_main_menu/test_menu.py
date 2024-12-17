import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from pathlib import Path
import sys
import os

# Импортируем класс MainMenu из вашего модуля
from main_menu.menu import MainMenu, Buttons
PATH_TO_UI = Path(__file__).parent.parent.parent / 'main_menu' / 'MainMenu.ui'


class TestMainMenu(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    @patch('PyQt5.QtWidgets.QMainWindow.close')
    def test_start_game(self, mock_close):
        window = MainMenu()
        window._start_game()
        self.assertEqual(window.button_clicked, Buttons.START)
        mock_close.assert_called_once()

    @patch('PyQt5.QtWidgets.QMainWindow.close')
    def test_open_editor(self, mock_close):
        window = MainMenu()
        window._open_editor()
        self.assertEqual(window.button_clicked, Buttons.EDITOR)
        mock_close.assert_called_once()

    def test_change_multiplayer_mode(self):
        window = MainMenu()
        with open(str(Path(__file__).parent.parent.parent / "game_src" / "config.ini"), "r") as f:
            f.readline()
            multiplayer = f.readline().split('=')[1].strip()

        window._change_multiplayer_mode(2)
        with open(str(Path(__file__).parent.parent.parent / "game_src" / "config.ini"), "r") as f:
            f.readline()
            self.assertEqual('True', f.readline().split('=')[1].strip())
        window._change_multiplayer_mode(0)
        with open(str(Path(__file__).parent.parent.parent / "game_src" / "config.ini"), "r") as f:
            f.readline()
            self.assertEqual('False', f.readline().split('=')[1].strip())
        window._change_multiplayer_mode(0 if multiplayer == "True" else 2)




if __name__ == '__main__':
    unittest.main()
