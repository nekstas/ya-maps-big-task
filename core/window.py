# -*- coding: utf-8 -*-
import os
from typing import Tuple

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QLabel

from ym.static_maps import show_map, YM_TMP_FILENAME


class Window(QMainWindow):
    ym_label: QLabel

    lo_la: Tuple[float, float]
    z: int
    map_type: str

    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.program_init()

    def program_init(self):
        self.lo_la = 0, 0
        self.z = 1
        self.map_type = 'map'
        self.update_ym()

    def update_ym(self):
        show_map(self.ym_label, self.lo_la, self.z)

    def closeEvent(self, event):
        os.remove(YM_TMP_FILENAME)
