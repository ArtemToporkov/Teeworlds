import asyncio
import os
import sys
from os.path import join
from threading import Thread

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QFileDialog, QWidget, QCheckBox

import web.server_src.server
from game_src.constants import SERVER_ADDR, ASSETS_PATH
from game_src.entities.map.map import Map


class ServerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.server = web.server_src.server.Server(*SERVER_ADDR)

        self.server_running = False
        self.init_ui()

    def init_ui(self):
        # Настройка окна
        self.setWindowTitle("Server Control")
        self.setGeometry(100, 100, 600, 400)

        # Основной виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #013220; 
            }
            QLabel, QCheckBox, QPushButton {
                color: white; 
                font-size: 25px;
            }
            QPushButton {
                background-color: #026b2e;
                border: 1px solid white;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #028c38;
            }
            QCheckBox {
                margin-left: 10px;
            }
        """)

        # Основной layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Кнопка запуска сервера
        self.start_server_btn = QPushButton()
        self.start_server_btn.setFixedSize(200, 200)
        self.start_server_btn.setIconSize(self.start_server_btn.size())
        self.start_server_btn.clicked.connect(self.toggle_server)
        self.update_button_image()
        layout.addWidget(self.start_server_btn, alignment=Qt.AlignCenter)

        self.random_items_checkbox = QCheckBox("Enable Buffs")
        self.random_items_checkbox.setChecked(True)
        self.random_items_checkbox.stateChanged.connect(self.toggle_random_items)

        self.ip_label = QLabel(f"IP: {self.server.ip}")
        self.port_label = QLabel(f"Port: {self.server.port}")
        self.map_label = QLabel("Map: None")

        # Помещаем эллементы на экран
        for widget in [self.ip_label, self.port_label, self.map_label, self.random_items_checkbox]:
            layout.addWidget(widget, alignment=Qt.AlignCenter)

        select_map_btn = QPushButton("Select Map")
        select_map_btn.clicked.connect(self.select_map)
        layout.addWidget(select_map_btn, alignment=Qt.AlignCenter)

        self.preload_map()

    def toggle_server(self):
        if not self.server_running:
            # Запуск сервера в отдельном потоке
            # self.server_thread = Thread(target=self.server.run, daemon=True)
            # self.server_thread.start()
            self.server_thread = Thread(target=self.start_server_loop, daemon=True)
            self.server_thread.start()
            self.server_running = True
        else:
            self.server.stop()
            self.server_running = False
        self.update_button_image()

    def start_server_loop(self):
        self.server_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.server_loop)
        try:
            self.server_loop.run_until_complete(self.server.run())
        except asyncio.CancelledError:
            pass
        finally:
            self.server_loop.close()

    def select_map(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Map", "./maps", "JSON_files (*.json)"
        )
        if file_path:
            self.server.map = Map.load_from_file(file_path)
            self.map_label.setText(os.path.basename(file_path))

    def preload_map(self):
        path = None
        base_map = "first level.json"
        try:
            path = join("maps", base_map)
        except FileNotFoundError:
            print(f'Map: {base_map}, not found')
            for file in os.listdir(path):
                if os.path.isfile(join(path, file)):
                    path = file

        self.map_label.setText(f"Map: {os.path.basename(path)}")
        self.server.map = Map.load_from_file(path)

    def update_button_image(self):
        path_to_icon = os.path.join(ASSETS_PATH, 'server_icon')
        if self.server_running:
            pixmap = QPixmap(join(path_to_icon, "server_off")).scaled(
                self.start_server_btn.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        else:
            pixmap = QPixmap(join(path_to_icon, "server_on")).scaled(
                self.start_server_btn.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )

        self.start_server_btn.setIcon(QIcon(pixmap))

    def toggle_random_items(self, state):
        if state == Qt.Checked:
            self.server.event_generator.enable()
        else:
            self.server.event_generator.disable()

    @staticmethod
    def run():
        app = QApplication(sys.argv)
        ui = ServerUI()
        ui.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    ServerUI.run()
