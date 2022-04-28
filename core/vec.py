# -*- coding: utf-8 -*-
# nekstas-site


class Vec:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other):
        if type(other) == int:
            return Vec(self.x * other, self.y * other)
        return Vec(self.x * other.x, self.y * other.y)

    def __imul__(self, other):
        if type(other) == int:
            self.x, self.y = self.x * other, self.y * other
        else:
            self.x, self.y = self.x * other.x, self.y * other.y
        return self

    def __truediv__(self, other):
        return Vec(self.x / other, self.y / other)

    def __itruediv__(self, other):
        self.x /= other
        self.y /= other
        return self

    @property
    def xy(self):
        return self.x, self.y