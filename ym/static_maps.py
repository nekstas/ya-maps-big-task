# -*- coding: utf-8 -*-
import sys

import requests
from PyQt5.QtGui import QPixmap

from core.constants import MAP_API_SERVER, YM_TMP_FILENAME, YM_IMG_SIZE


def show_map(ym_label, bbox, dot, map_type='map'):
    params = {
        'bbox': bbox.to_ym(),
        'l': map_type,
        'size': YM_IMG_SIZE
    }

    response = requests.get(MAP_API_SERVER, params=params)

    if not response:
        print('Произошла ошибка при получении карты.')
        print(f'{response.status_code}: {response.reason}')
        print(response.text)
        sys.exit(1)

    with open(YM_TMP_FILENAME, 'wb') as o_file:
        o_file.write(response.content)

    ym_label.setPixmap(QPixmap(YM_TMP_FILENAME))
