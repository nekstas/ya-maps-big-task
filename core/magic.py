# -*- coding: utf-8 -*-
from math import sin, log, pi, tan

from core.constants import YM_IMG_SIZE_V
from core.vec import Vec

e = 0.0818191908426
Z = 32


def lola_to_xy(z, long, lat):
    """ Магия для превращения географических координат
        в пиксельные координаты """
    b = pi * lat / 180
    phi = (1 - e * sin(b)) / (1 + e * sin(b))
    te = tan(pi / 4 + b / 2) * phi ** (e / 2)
    p = 2 ** (z + 8) / 2

    x = p * (1 + long / 180)
    y = p * (1 - log(te) / pi)

    return x, y


def xy_to_lola(z, x, y):
    """ Магия для превращения пиксельных координат
        в географические координаты """
    bl, br = -180, 180
    for i in range(Z + z):
        m = (bl + br) / 2
        mx, _ = lola_to_xy(z, m, 0)

        if mx <= x:
            bl = m
        else:
            br = m
    long = bl

    bl, br = -85, 85
    for i in range(Z + z):
        m = (bl + br) / 2
        _, my = lola_to_xy(z, 0, m)

        if my >= y:
            bl = m
        else:
            br = m
    lat = br

    return long, lat


def lola_to_spn(z, long, lat):
    """ Магия для определения размера видимой области """
    x, y = lola_to_xy(z, long, lat)
    return Vec(*xy_to_lola(
        z,
        x + YM_IMG_SIZE_V.x / 2,
        y - YM_IMG_SIZE_V.y / 2
    )) - Vec(*xy_to_lola(
        z,
        x - YM_IMG_SIZE_V.x / 2,
        y + YM_IMG_SIZE_V.y / 2
    ))
