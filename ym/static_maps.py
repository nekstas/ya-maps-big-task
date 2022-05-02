# -*- coding: utf-8 -*-
import sys
from math import cos, radians, sin

import requests
from PyQt5.QtGui import QPixmap

from core.constants import MAP_API_SERVER, YM_TMP_FILENAME, \
    YM_IMG_SIZE, MAGIC_DV
from core.rect import Rect
from core.vec import Vec


def show_map(ym_label, bbox, dot=None, map_type='map'):
    bbox = Rect.from_center(
        bbox.center,
        bbox.size / MAGIC_DV
    )

    params = {
        'bbox': bbox.to_ym(),
        'l': map_type,
        'size': YM_IMG_SIZE
    }

    if dot:
        params['pt'] = f'{dot.x},{dot.y},pm2gnm'

    response = requests.get(MAP_API_SERVER, params=params)

    if not response:
        print('Произошла ошибка при получении карты.')
        print(f'{response.status_code}: {response.reason}')
        print(response.text)
        sys.exit(1)

    print(response.url)

    with open(YM_TMP_FILENAME, 'wb') as o_file:
        o_file.write(response.content)

    ym_label.setPixmap(QPixmap(YM_TMP_FILENAME))
