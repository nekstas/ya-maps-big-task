# -*- coding: utf-8 -*-
import sys

import requests
from PyQt5.QtGui import QPixmap

MAP_API_SERVER = 'http://static-maps.yandex.ru/1.x/'
YM_TMP_FILENAME = 'ym-tmp.png'


def show_map(ym_label, lo_la, z=1, map_type='map'):
    params = {
        'll': ','.join(map(str, lo_la)),
        'z': z,
        'l': map_type
    }

    response = requests.get(MAP_API_SERVER, params=params)

    if not response:
        print('Произошла ошибка при получении карты.')
        print(f'{response.status_code}: {response.reason}')
        sys.exit(1)

    with open(YM_TMP_FILENAME, 'wb') as o_file:
        o_file.write(response.content)

    ym_label.setPixmap(QPixmap(YM_TMP_FILENAME))
