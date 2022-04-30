# -*- coding: utf-8 -*-
import os

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import Qt

from core.rect import Rect
from core.vec import Vec
from ym.static_maps import show_map, YM_TMP_FILENAME


class Window(QMainWindow):
    ym_label: QLabel

    bbox: Rect
    map_type: str

    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.program_init()

    def program_init(self):
        self.bbox = Rect(Vec(-80, -80), Vec(160, 160))
        self.map_type = 'map'
        self.update_ym()

    def update_ym(self):
        show_map(self.ym_label, self.bbox)

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
        else:
            return

        self.update_ym()

    def check_borders(self):
        if (self.bbox.pos.x < -180) or (self.bbox.pos.y < -80):
            return False

        if (self.bbox.pos.x + self.bbox.size.x > 180) or \
                (self.bbox.pos.y + self.bbox.size.y > 90):
            return False

        if self.bbox.size.x < 160 / 2 ** 15 or \
                self.bbox.size.y < 160 / 2 ** 15:
            return False

        return True
