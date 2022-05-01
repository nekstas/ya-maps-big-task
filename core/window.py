# -*- coding: utf-8 -*-
import os
from typing import Optional

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QComboBox
from PyQt5.QtCore import Qt

from core.constants import MAP_LAYERS
from core.rect import Rect
from core.vec import Vec

from ym.geocoder import get_toponym, get_toponym_spn, get_toponym_lo_la
from ym.static_maps import show_map, YM_TMP_FILENAME


class Window(QMainWindow):
    ym_label: QLabel
    options_layout: QVBoxLayout
    layer_input: QComboBox

    bbox: Rect
    map_type: str
    dot: Optional[str]

    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.program_init()

    def program_init(self):
        self.options_layout.setAlignment(Qt.AlignTop)
        self.layer_input.currentIndexChanged.connect(self.layer_changed)
        self.find_button.clicked.connect(self.find)
        self.dot = None

        self.bbox = Rect.from_center(Vec(), Vec(160, 160))
        self.map_type = MAP_LAYERS[self.layer_input.currentIndex()]
        self.update_ym()

    def update_ym(self):
        show_map(self.ym_label, self.bbox, self.dot, self.map_type)

    def closeEvent(self, event):
        os.remove(YM_TMP_FILENAME)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.bbox /= 2
            if not self.check_borders():
                self.bbox *= 2
        elif event.key() == Qt.Key_PageDown:
            self.bbox *= 2
            if not self.check_borders():
                self.bbox /= 2
        elif event.key() == Qt.Key_Left:
            self.bbox.move(Vec(-1, 0))
            if not self.check_borders():
                self.bbox.move(Vec(1, 0))
        elif event.key() == Qt.Key_Right:
            self.bbox.move(Vec(1, 0))
            if not self.check_borders():
                self.bbox.move(Vec(-1, 0))
        elif event.key() == Qt.Key_Up:
            self.bbox.move(Vec(0, 1))
            if not self.check_borders():
                self.bbox.move(Vec(0, -1))
        elif event.key() == Qt.Key_Down:
            self.bbox.move(Vec(0, -1))
            if not self.check_borders():
                self.bbox.move(Vec(0, 1))
        else:
            return

        self.update_ym()

    def check_borders(self):
        if (self.bbox.pos.x < -180) or (self.bbox.pos.y < -80):
            return False

        if (self.bbox.pos.x + self.bbox.size.x > 180) or \
                (self.bbox.pos.y + self.bbox.size.y > 90):
            return False

        if self.bbox.size.x < 160 / 2 ** 17 or \
                self.bbox.size.y < 160 / 2 ** 17:
            return False

        return True

    def layer_changed(self, index):
        self.map_type = MAP_LAYERS[index]
        self.update_ym()

    def find(self):
        toponym = get_toponym(self.address_input().text())
        coords = get_toponym_lo_la(toponym)
        obj_size = get_toponym_spn(toponym)
        point = f"{coords[0]},{coords[1]}"
        color = 'pm2gnm'
        self.dot = f'{point},{color}'
        self.update_ym()
        self.bbox.change_center(coords)
        while obj_size[0] < self.bbox.size.x or obj_size[1] < self.bbox.size.y:
            self.bbox.size *= 2
        while obj_size[0] > self.bbox.size.x or obj_size[1] > self.bbox.size.y:
            self.bbox.size /= 2
        while not self.check_borders():
            self.bbox.size /= 2
