# import unittest
# from unittest.mock import MagicMock, patch
# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QCheckBox, QPushButton, QLabel
#
# from web.server_src.ui import ServerUI
#
#
# class TestServerUI(unittest.TestCase):
#     @patch("web.server_src.server.Server")
#     @patch("web.server_src.ui.QFileDialog.getOpenFileName")
#     @patch('PyQt5.QtWidgets.super')
#     def setUp(self, mock_file_dialog, mock_server, _):
#         self.ui = ServerUI()
#
#         self.mock_server = mock_server.return_value
#         self.mock_file_dialog = mock_file_dialog
#
#         # Замокать GUI элементы
#         self.ui.start_server_btn = MagicMock(spec=QPushButton)
#         self.ui.random_items_checkbox = MagicMock(spec=QCheckBox)
#         self.ui.ip_label = MagicMock(spec=QLabel)
#         self.ui.port_label = MagicMock(spec=QLabel)
#         self.ui.map_label = MagicMock(spec=QLabel)
#
#     def test_toggle_server(self):
#         # Тестируем включение и выключение сервера
#         self.ui.server_running = False
#         self.ui.toggle_server()
#         self.assertTrue(self.ui.server_running)
#         self.mock_server.run.assert_called_once()
#
#         self.ui.toggle_server()
#         self.assertFalse(self.ui.server_running)
#         self.mock_server.stop.assert_called_once()
#
#     def test_select_map(self):
#         # Тестируем выбор карты
#         self.mock_file_dialog.return_value = ("test_map.json", None)
#         self.ui.select_map()
#
#         self.mock_server.map.load_from_file.assert_called_once_with("test_map.json")
#         self.ui.map_label.setText.assert_called_once_with("test_map.json")
#
#     def test_preload_map(self):
#         with patch("server_ui.join", return_value="maps/first level.json") as mock_join:
#             with patch("server_ui.os.path.basename", return_value="first level.json"):
#                 self.ui.preload_map()
#
#                 self.mock_server.map.load_from_file.assert_called_once_with("maps/first level.json")
#                 self.ui.map_label.setText.assert_called_once_with("Map: first level.json")
#
#     def test_update_button_image(self):
#         # Тестируем обновление иконки кнопки
#         with patch("server_ui.join", return_value="path/to/icon") as mock_join:
#             with patch("server_ui.QPixmap") as mock_pixmap:
#                 self.ui.server_running = True
#                 self.ui.update_button_image()
#                 mock_pixmap.assert_called_with("path/to/icon/server_off")
#
#                 self.ui.server_running = False
#                 self.ui.update_button_image()
#                 mock_pixmap.assert_called_with("path/to/icon/server_on")
#
#     def test_toggle_random_items(self):
#         # Тестируем включение/выключение генерации событий
#         self.ui.toggle_random_items(Qt.Checked)
#         self.mock_server.event_generator.enable.assert_called_once()
#
#         self.ui.toggle_random_items(Qt.Unchecked)
#         self.mock_server.event_generator.disable.assert_called_once()
#
#
# if __name__ == "__main__":
#     unittest.main()
