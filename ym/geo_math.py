# -*- coding: utf-8 -*-
from math import cos, radians, sqrt


def lo_la_distance(point1, point2):
    d_to_m_factor = 111e3
    a_lo, a_la = point1.xy
    b_lo, b_la = point2.xy

    la_lo_factor = cos(radians((a_la + b_la) / 2))

    dx = abs(a_lo - b_lo) * d_to_m_factor * la_lo_factor
    dy = abs(a_la - b_la) * d_to_m_factor

    return sqrt(dx * dx + dy * dy)
