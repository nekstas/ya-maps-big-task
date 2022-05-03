# -*- coding: utf-8 -*-
# Автор: Некрасов Станислав
import sys

import requests

from core.constants import SEARCH_MAPS_APIKEY, SEARCH_API_SERVER


def search_org(text, lo_la):
    params = {
        'apikey': SEARCH_MAPS_APIKEY,
        'text': text,
        'lang': 'ru_RU',
        'll': lo_la.to_ym(),
        'type': 'biz'
    }

    response = requests.get(SEARCH_API_SERVER, params=params)

    if not response:
        print('Произошла ошибка при выполнении поиска.')
        print(f'{response.status_code}: {response.reason}')
        sys.exit()

    json_response = response.json()

    try:
        return json_response['features'][0]
    except IndexError:
        return
