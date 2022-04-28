# -*- coding: utf-8 -*-
# nekstas-site

class Rect:
    def __init__(self, pos, size):
        self.pos, self.size = pos, size

    def __itruediv__(self, k):
        center = self.pos + self.size / 2
        self.size /= k
        self.pos = center - self.size / 2
        return self

    def __imul__(self, k):
        center = self.pos + self.size / 2
        self.size *= k
        self.pos = center - self.size / 2
        return self

    @property
    def coords(self):
        return self.pos, self.pos + self.size

    def to_ym(self):
        coords = self.coords
        return f'{coords[0].x},{coords[0].y}~' \
               f'{coords[1].x},{coords[1].y}'

    def move(self, v):
        self.pos += self.size * v
