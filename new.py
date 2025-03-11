from random import choice

import pygame

from support import *

cities = [elem.strip() for elem in open('cities.txt', encoding='utf8').readlines()]


def get_map(city):
    toponym = get_geocode_json(city)
    toponym_coodrinates = toponym["Point"]["pos"]
    spn = ','.join(map(lambda x: str(float(x) / 10),
                       get_spn(toponym['boundedBy']['Envelope']['lowerCorner'],
                               toponym['boundedBy']['Envelope']['upperCorner']).split(',')))
    response = get_staticmap(toponym_coodrinates, spn)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


def show_map(map_file):
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    running = True
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                get_map(choice(cities))
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()


if __name__ == '__main__':
    get_map(choice(cities))
    show_map('map.png')
