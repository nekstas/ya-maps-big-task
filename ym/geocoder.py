import sys
import requests

from core.constants import GEOCODER_API_SERVER, GEOCODER_APIKEY
from core.vec import Vec


def get_toponym(address):
    params = {
        "apikey": GEOCODER_APIKEY,
        "geocode": address,
        "format": "json"
    }

    response = requests.get(GEOCODER_API_SERVER, params=params)

    if not response:
        print("Ошибка получения топонима:")
        print(response.url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit()

    json_response = response.json()

    return json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]


def get_toponym_lo_la(toponym):
    toponym_pos = toponym["Point"]["pos"]
    lo, la = map(float, toponym_pos.split(" "))

    return Vec(lo, la)


def get_toponym_spn(toponym):
    corners = toponym["boundedBy"]["Envelope"]
    lc = [*map(float, corners["lowerCorner"].split())]
    uc = [*map(float, corners["upperCorner"].split())]

    return Vec(uc[0] - lc[0], uc[1] - lc[1])
