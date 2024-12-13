import json
import os
import sys
import time
from functools import partial

import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QWizardPage, QGraphicsScene, QGraphicsPixmapItem, QInputDialog, \
    QLineEdit, QMessageBox
from PyQt5.uic import loadUi
from pathlib import Path
from PyQt5.QtGui import QPixmap

from game_src.constants import ASSETS_PATH
from game_src.entities.map.map import Map
from game_src.entities.map.platform import Platform
from geometry.vector import Vector
from levels_editor.src import src
from buttons_enum import Buttons
from styles import MAP_SAVING_DIALOG_STYLE


class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        ui = Path(__file__).parent / 'editor.ui'
        loadUi(ui, self)
        self._connect_platforms_and_spawn_buttons()
        self.scene = self._set_map_scene()
        self.spawn = self._set_spawn()
        self.exitButton.clicked.connect(lambda _: self.close())  # TODO: сделать так чтобы на exit открывалось меню
        self.saveButton.clicked.connect(self._save)
        self.map.mousePressEvent = self._on_map_clicked
        self.current_selected_item = None
        self.platforms: dict[(int, int), Platform] = dict()

    def _connect_platforms_and_spawn_buttons(self):
        for button in [
            self.firstPlatform, self.secondPlatform, self.thirdPlatform, self.fourthPlatform, self.fifthPlatform,
            self.sixthPlatform, self.seventhPlatform, self.spawnButton, self.deleteButton
        ]:
            button.clicked.connect(partial(self._on_button_clicked, button))

    def _on_button_clicked(self, button):
        self.current_selected_item = button.objectName()
        print(button.objectName())

    def _on_map_clicked(self, event):
        placement_position = self.map.mapToScene(event.pos())
        print(self.platforms)
        match self.current_selected_item:
            case None:
                return
            case Buttons.DELETE_BUTTON:
                for item in [i for i in self.scene.items(placement_position) if i != self.spawn]:
                    self.scene.removeItem(item)
                    if (item.x(), item.y()) in self.platforms.keys():
                        del self.platforms[item.x(), item.y()]
            case _ if self.current_selected_item in [button for button in Buttons]:
                qpixmap = QPixmap(BUTTONS_NAMES_AND_PATHS[self.current_selected_item])
                width, height = qpixmap.width(), qpixmap.height()
                placement_position = Vector(placement_position.x() - width / 2, placement_position.y() - height / 2)
                if self.current_selected_item == Buttons.SPAWN_BUTTON:
                    self._change_spawn_coordinates(placement_position.x, placement_position.y)
                    return
                item = QGraphicsPixmapItem(qpixmap)
                item.setPos(placement_position.x, placement_position.y)
                self.scene.addItem(item)
                if item.collidingItems():
                    self.scene.removeItem(item)
                else:
                    self.platforms[(placement_position.x, placement_position.y)] = Platform(
                        placement_position.x, placement_position.y,
                        width, height, BUTTONS_NAMES_AND_PATHS[self.current_selected_item]
                    )
            case _:
                return

    def _set_map_scene(self) -> QGraphicsScene:
        scene = QGraphicsScene()
        scene.setSceneRect(0, 0, 1800, 1300)
        self.map.scale(0.5, 0.5)
        self.map.setScene(scene)
        return scene

    def _set_spawn(self) -> QGraphicsPixmapItem:
        qpixmap = QPixmap(BUTTONS_NAMES_AND_PATHS[Buttons.SPAWN_BUTTON])
        spawn = QGraphicsPixmapItem(qpixmap)
        position = self.map.mapToScene(500 - int(qpixmap.width() / 2), 350 - int(qpixmap.height() / 2))
        spawn.setPos(position)
        self.scene.addItem(spawn)
        return spawn

    def _change_spawn_coordinates(self, x, y) -> None:
        old_x, old_y = self.spawn.pos().x(), self.spawn.pos().y()
        self.spawn.setPos(x, y)
        if self.spawn.collidingItems():
            self.spawn.setPos(old_x, old_y)

    def _save(self):
        dialog = QInputDialog(self)
        dialog.setStyleSheet(MAP_SAVING_DIALOG_STYLE)
        dialog.setWindowTitle("Save?")
        dialog.setLabelText("Enter a new map name:")
        # блокировка основного окна на время работы диалога + проверка на нажатие OK:
        if dialog.exec_() == QInputDialog.Accepted:
            map_name = dialog.textValue()
            if map_name:
                map = Map(list(self.platforms.values()), Vector(self.spawn.x(), self.spawn.y()))
                with open(os.path.join(ASSETS_PATH, 'maps', f'{map_name}.json'), 'w') as file:
                    js = json.dumps(map.to_dict(), indent=4)
                    file.write(js)
            else:
                QMessageBox.critical(self, 'WARNING!', f'Map didn\'t save: the name can\'t be empty.')


BUTTONS_NAMES_AND_PATHS = {
    Buttons.FIRST_PLATFORM: str(Path(__file__).parent / 'src' / '1.png'),
    Buttons.SECOND_PLATFORM: str(Path(__file__).parent / 'src' / '3.png'),
    Buttons.THIRD_PLATFORM: str(Path(__file__).parent / 'src' / '4.png'),
    Buttons.FOURTH_PLATFORM: str(Path(__file__).parent / 'src' / '5.png'),
    Buttons.FIFTH_PLATFORM: str(Path(__file__).parent / 'src' / '6.png'),
    Buttons.SIXTH_PLATFORM: str(Path(__file__).parent / 'src' / '7.png'),
    Buttons.SEVENTH_PLATFORM: str(Path(__file__).parent / 'src' / '8.png'),
    Buttons.SPAWN_BUTTON: str(Path(__file__).parent / 'src' / 'spawn.png')
}


def main():
    app = QApplication(sys.argv)
    window = Editor()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
