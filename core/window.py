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
            pass  # Новый код для увеличения масштаба
        elif event.key() == Qt.Key_PageDown:
            pass  # Новый код для уменьшения масштаба
        else:
            return

        self.update_ym()
