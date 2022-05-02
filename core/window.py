# -*- coding: utf-8 -*-
import os
from typing import Optional

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, \
    QComboBox, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt

from core.constants import MAP_LAYERS, YM_IMG_SIZE_V
from core.magic import lola_to_xy, xy_to_lola, lola_to_spn
from core.vec import Vec

from ym.geocoder import get_toponym, get_toponym_spn, get_toponym_lo_la
from ym.static_maps import show_map, YM_TMP_FILENAME


class Window(QMainWindow):
    ym_label: QLabel
    options_layout: QVBoxLayout
    layer_input: QComboBox
    address_input: QLineEdit

    z: int
    lola: Vec
    map_type: str
    dot: Optional[Vec]

    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.program_init()

    def program_init(self):
        self.options_layout.setAlignment(Qt.AlignTop)
        self.layer_input.currentIndexChanged.connect(self.layer_changed)
        self.find_button.clicked.connect(self.find_obj)
        self.delete_button.clicked.connect(self.delete_dot)

        self.z = 0
        self.lola = Vec(0, 0)
        self.dot = None
        self.map_type = MAP_LAYERS[self.layer_input.currentIndex()]
        self.update_ym()

    def update_ym(self):
        show_map(self.ym_label, self.z, self.lola, self.dot, self.map_type)

    def closeEvent(self, event):
        os.remove(YM_TMP_FILENAME)

    def move_ym(self, v):
        old_lola = self.lola

        v *= YM_IMG_SIZE_V
        x, y = lola_to_xy(self.z, *self.lola.xy)
        x, y = x + v.x, y + v.y

        self.lola = Vec(*xy_to_lola(self.z, x, y))
        if not self.check_borders():
            self.lola = old_lola

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.z += 1
            if not self.check_borders():
                self.z -= 1
        elif event.key() == Qt.Key_PageDown:
            self.z -= 1
            if not self.check_borders():
                self.z += 1
        elif event.key() == Qt.Key_Left:
            self.move_ym(Vec(-1, 0))
        elif event.key() == Qt.Key_Right:
            self.move_ym(Vec(1, 0))
        elif event.key() == Qt.Key_Up:
            self.move_ym(Vec(0, -1))
        elif event.key() == Qt.Key_Down:
            self.move_ym(Vec(0, 1))
        else:
            return

        self.update_ym()

    def check_borders(self):
        return not (
            abs(abs(self.lola.x) - 180) < 0.5 or
            abs(abs(self.lola.y) - 85) < 0.5 or
            not (0 <= self.z <= 17)
        )

    def layer_changed(self, index):
        self.map_type = MAP_LAYERS[index]
        self.update_ym()

    def compare_spn(self, obj_size, cmp):
        ym_spn = lola_to_spn(self.z, *self.lola.xy)

        return (cmp == -1 and (
            ym_spn.x < obj_size.x or
            ym_spn.y < obj_size.y
        )) or (cmp == 1 and (
            ym_spn.x > obj_size.x or
            ym_spn.y > obj_size.y
        ))

    def find_obj(self):
        try:
            toponym = get_toponym(self.address_input.text())
        except IndexError:
            QMessageBox.critical(
                self,
                'Ошибка',
                'Извините, но объект по данному запросу не найден'
            )
            return

        coords = get_toponym_lo_la(toponym)
        obj_size = get_toponym_spn(toponym)

        self.dot = self.lola = coords

        while self.compare_spn(obj_size, 1):
            self.z += 1
        while self.compare_spn(obj_size, -1):
            self.z -= 1

        self.update_ym()

    def delete_dot(self):
        self.dot = None

        self.update_ym()
