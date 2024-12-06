from threading import Thread

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QFileDialog, QWidget, QCheckBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from os.path import join
import server_src.server
import os
import sys


class ServerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.server = server_src.server.Server("localhost", 8686)

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

        # Тумблер для рандомных предметов
        self.random_items_checkbox = QCheckBox("Enable Buffs")
        self.random_items_checkbox.setChecked(False)
        self.random_items_checkbox.stateChanged.connect(self.toggle_random_items)

        # Лейблы с информацией
        self.ip_label = QLabel(f"IP: {self.server.ip}")
        self.port_label = QLabel(f"Port: {self.server.port}")
        self.map_label = QLabel("Map: None")
        self.mode_label = QLabel("Mode: Single")

        # Помещаем эллементы на экран
        for widget in [self.ip_label, self.port_label, self.map_label, self.mode_label, self.random_items_checkbox]:
            layout.addWidget(widget, alignment=Qt.AlignCenter)

        # Кнопка выбора карты
        select_map_btn = QPushButton("Select Map")
        select_map_btn.clicked.connect(self.select_map)
        layout.addWidget(select_map_btn, alignment=Qt.AlignCenter)

        self.preload_map()

    def toggle_server(self):
        if not self.server_running:
            # Запуск сервера в отдельном потоке
            self.server_thread = Thread(target=self.server.run, daemon=True)
            self.server_thread.start()
            self.server_running = True
        else:
            self.server.stop()
            self.server_running = False
        self.update_button_image()

    def change_mode(self):
        self.server.change_mode()
        mode_text = "Single" if self.server.mode == 0 else "Team"
        self.mode_label.setText(f"Mode: {mode_text}")

    def select_map(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Map", join("assets", "maps"), "TXT Files (*.txt)"
        )
        if file_path:
            with open(file_path, "r") as f:
                self.server.map_lines = f.readlines()
            self.server.map.load_from_list(self.server.map_lines, w_sprites=False)
            self.map_label.setText(f"Map: {os.path.basename(file_path)}")

    def preload_map(self):
        path = join("assets", "maps")
        for file in os.listdir(path):
            if os.path.isfile(join(path, file)):
                self.map_label.setText(f"Map: {file}")
                with open(join(path, file), "r") as f:
                    self.server.map_lines = f.readlines()
                self.server.map.load_from_list(self.server.map_lines, w_sprites=False)
                break

    def update_button_image(self):
        path_to_icon = 'assets/server_icon'
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
            self.server.buff_spawner.enable()
            self.server.event_generator.enable()
        else:
            self.server.buff_spawner.disable()
            self.server.event_generator.disable()

    @staticmethod
    def run():
        app = QApplication(sys.argv)
        ui = ServerUI()
        ui.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    ServerUI.run()
