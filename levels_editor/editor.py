import sys
import time
from functools import partial

import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QWizardPage, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from PyQt5.uic import loadUi
from pathlib import Path
from PyQt5.QtGui import QPixmap
from levels_editor.src import src
from buttons_enum import Buttons


class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        ui = Path(__file__).parent / 'editor.ui'
        loadUi(ui, self)
        self._connect_platforms_and_spawn_buttons()
        self.scene = self._set_map_scene()
        self.spawn = self._set_spawn()
        self.exitButton.clicked.connect(lambda _: self.close())  # TODO: сделать так чтобы на exit открывалось меню
        self.map.mousePressEvent = self._on_map_clicked
        self.current_selected_item = None

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
        match self.current_selected_item:
            case None:
                return
            case Buttons.DELETE_BUTTON:
                for item in [i for i in self.scene.items(placement_position) if i != self.spawn]:
                    self.scene.removeItem(item)
            case _ if self.current_selected_item in [button for button in Buttons]:
                qpixmap = QPixmap(PLATFORMS_NAMES_AND_PIXMAPS[self.current_selected_item])
                scale_coef = 0.5
                width, height = qpixmap.width() * scale_coef, qpixmap.height() * scale_coef
                if self.current_selected_item == Buttons.SPAWN_BUTTON:
                    self._change_spawn_coordinates(placement_position.x() - width / 2, placement_position.y() - height / 2)
                    return
                item = QGraphicsPixmapItem(qpixmap)
                item.setScale(0.5)
                item.setPos(placement_position.x() - width / 2, placement_position.y() - height / 2)
                self.scene.addItem(item)
                if item.collidingItems():
                    self.scene.removeItem(item)
            case _:
                return

    def _set_map_scene(self) -> QGraphicsScene:
        scene = QGraphicsScene()
        scene.setSceneRect(0, 0, 900, 650)
        self.map.setScene(scene)
        return scene

    def _set_spawn(self) -> QGraphicsPixmapItem:
        spawn = QGraphicsPixmapItem(QPixmap(PLATFORMS_NAMES_AND_PIXMAPS[Buttons.SPAWN_BUTTON]))
        position = self.map.mapToScene(430, 300)
        scale_coef = 0.5
        spawn.setPos(position)
        spawn.setScale(scale_coef)
        self.scene.addItem(spawn)
        return spawn

    def _change_spawn_coordinates(self, x, y) -> None:
        old_x, old_y = self.spawn.pos().x(), self.spawn.pos().y()
        self.spawn.setPos(x, y)
        if self.spawn.collidingItems():
            self.spawn.setPos(old_x, old_y)


PLATFORMS_NAMES_AND_PIXMAPS = {
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
