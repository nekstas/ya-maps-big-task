# -*- coding: utf-8 -*-
from math import cos, radians

from core.constants import MAGIC_DV
from core.vec import Vec


class Rect:
    def __init__(self, pos, size):
        self.pos, self.size = pos, size

    def __itruediv__(self, k):
        return Rect.from_center(self.center, self.size / k)

    def __imul__(self, k):
        return Rect.from_center(self.center, self.size * k)

    @property
    def coords(self):
        return self.pos, self.pos + self.size

    @property
    def center(self):
        return self.pos + self.size / 2

    def to_ym(self):
        coords = self.coords
        return f'{coords[0].x},{coords[0].y}~' \
               f'{coords[1].x},{coords[1].y}'

    def move(self, v):
        self.pos += self.size * v

    @staticmethod
    def from_center(center, size):
        return Rect(center - size / 2, size)

    def change_center(self, center):
        self.pos = center - self.size / 2
