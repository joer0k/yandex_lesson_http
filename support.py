import sys
import math
import requests


def get_geocode_json(arg: str):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": 'd2f5711d-9e67-414c-aa2c-d7c0465aea3e',
        "geocode": arg,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        print(f'Ошибка выполнения запроса: {response.content}')
        sys.exit(1)
    return response.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]


def get_spn(lowerCorner: str, upperCorner: str) -> str:
    left, button = lowerCorner.split()
    right, top = upperCorner.split()
    dx = abs(float(right) - float(left))
    dy = abs(float(top) - float(button))
    return f'{dx}, {dy}'


def get_staticmap(coords_place, coords_pharmacy):
    apikey = "371e1360-5397-45a5-9639-2e7da34bd060"
    map_params = {
        # "ll": ",".join(coords.split(' ')),
        # "spn": spn,
        "apikey": apikey,
        'pt': f'{",".join(coords_place.split(" "))},home'
              f'~{coords_pharmacy[0][0]},{coords_pharmacy[0][1]}'
              f'~{coords_pharmacy[1][0]},{coords_pharmacy[1][1]}'
              f'~{coords_pharmacy[2][0]},{coords_pharmacy[2][1]}'
              f'~{coords_pharmacy[3][0]},{coords_pharmacy[3][1]}'
              f'~{coords_pharmacy[4][0]},{coords_pharmacy[4][1]}'
              f'~{coords_pharmacy[5][0]},{coords_pharmacy[5][1]}'
              f'~{coords_pharmacy[6][0]},{coords_pharmacy[6][1]}'
              f'~{coords_pharmacy[7][0]},{coords_pharmacy[7][1]}'
              f'~{coords_pharmacy[8][0]},{coords_pharmacy[8][1]}'
              f'~{coords_pharmacy[9][0]},{coords_pharmacy[9][1]}'
    }
    map_api_server = "https://static-maps.yandex.ru/v1"
    response = requests.get(map_api_server, params=map_params)
    if not response:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    return response


def search_organization(spn, ll, organization):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    search_params = {
        "apikey": api_key,
        "text": organization,
        "lang": "ru_RU",
        "ll": ll,
        "type": "biz",
        'spn': spn,
    }
    response = requests.get(search_api_server, params=search_params)
    if not response:
        print(f"Ошибка выполнения запроса: {response.content}")
        sys.exit(1)
    return response.json()["features"]


def get_distance(a, b):
    degree_to_meters = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon = math.cos(radians_lattitude)
    dx = abs(a_lon - b_lon) * degree_to_meters * lat_lon
    dy = abs(a_lat - b_lat) * degree_to_meters
    dist = math.sqrt(dx ** 2 + dy ** 2)
    return dist
