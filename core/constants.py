# -*- coding: utf-8 -*-
from core.vec import Vec

# Яндекс.Карты
MAP_API_SERVER = 'https://static-maps.yandex.ru/1.x/'
YM_TMP_FILENAME = 'ym-tmp.png'

# Магические константы для Яндекс.Карт
MAGIC_DX = 600 / 229  # 2.6200873362445414
MAGIC_DY = 450 / 236  # 1.9067796610169492
MAGIC_DV = Vec(MAGIC_DX, MAGIC_DY)
