import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import PyQt5
from PyQt5.QtWidgets import QApplication, QInputDialog
from PyQt5.QtWidgets import QGraphicsPixmapItem

from levels_editor.buttons_enum import Buttons
from levels_editor.editor import Editor


class TestEditor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()

    def setUp(self):
        self.editor = Editor()

    def test_connect_platforms_and_spawn_buttons(self):
        buttons = [
            self.editor.firstPlatform, self.editor.secondPlatform, self.editor.thirdPlatform,
            self.editor.fourthPlatform, self.editor.fifthPlatform, self.editor.sixthPlatform,
            self.editor.seventhPlatform, self.editor.spawnButton, self.editor.deleteButton
        ]
        for button in buttons:
            self.assertTrue(button.clicked.connect)

    def test_on_button_clicked(self):
        button = MagicMock()
        button.objectName.return_value = 'test_button'
        self.editor._on_button_clicked(button)
        self.assertEqual(self.editor.current_selected_item, 'test_button')

    def test_on_map_clicked_delete_button(self):
        event = MagicMock()
        event.pos.return_value = PyQt5.QtCore.QPoint(10, 10)
        self.editor.current_selected_item = Buttons.FIFTH_PLATFORM
        self.editor._on_map_clicked(event)
        self.editor.current_selected_item = Buttons.DELETE_BUTTON
        self.editor._on_map_clicked(event)
        self.assertEqual(len(self.editor.platforms), 0)

    def test_on_map_clicked_platform_button(self):
        event = MagicMock()
        event.pos.return_value = PyQt5.QtCore.QPoint(10, 10)
        self.editor.current_selected_item = Buttons.FIRST_PLATFORM
        self.editor._on_map_clicked(event)
        self.assertGreater(len(self.editor.platforms), 0)

    def test_set_map_scene(self):
        scene = self.editor._set_map_scene()
        self.assertEqual(scene.sceneRect(), PyQt5.QtCore.QRectF(0.0, 0.0, 1800.0, 1300.0))

    def test_set_spawn(self):
        spawn = self.editor._set_spawn()
        self.assertIsInstance(spawn, QGraphicsPixmapItem)

    def test_change_spawn_coordinates(self):
        old_x, old_y = self.editor.spawn.pos().x(), self.editor.spawn.pos().y()
        self.editor._change_spawn_coordinates(100, 100)
        self.assertEqual(self.editor.spawn.pos().x(), 100)
        self.assertEqual(self.editor.spawn.pos().y(), 100)
        self.editor._change_spawn_coordinates(old_x, old_y)

    @patch('PyQt5.QtWidgets.QInputDialog.exec_')
    @patch('PyQt5.QtWidgets.QInputDialog.textValue')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_save(self, mock_open, mock_text_value, mock_exec):
        mock_exec.return_value = QInputDialog.Accepted
        mock_text_value.return_value = 'test_map'
        self.editor._save()
        mock_open.assert_called_once_with(str(Path(__file__).parent.parent.parent / 'maps' / 'test_map.json'), 'w')

    @patch('PyQt5.QtWidgets.QInputDialog.exec_')
    @patch('PyQt5.QtWidgets.QMessageBox.critical')
    def test_save_empty_name(self, mock_critical, mock_exec):
        mock_exec.return_value = QInputDialog.Accepted
        self.editor._save()
        mock_critical.assert_called_once_with(self.editor, 'WARNING!', "Map didn't save: the name can't be empty.")


if __name__ == '__main__':
    unittest.main()
