import pygame

from support import *

toponym_to_find = " ".join(sys.argv[1:])
toponym = get_geocode_json(toponym_to_find)
toponym_coodrinates = toponym["Point"]["pos"]
spn = ','.join(map(lambda x: str(float(x) / 10),
                   get_spn(toponym['boundedBy']['Envelope']['lowerCorner'],
                           toponym['boundedBy']['Envelope']['upperCorner']).split(',')))

res = search_organization(spn, ','.join(toponym_coodrinates.split()), 'Аптека')
coords = []


def get_type_point(elem):
    if 'TwentyFourHours' in elem['properties']['CompanyMetaData']['Hours']['Availabilities'][0]:
        return 'pmgnm'
    if 'Intervals' in elem['properties']['CompanyMetaData']['Hours']['Availabilities'][0]:
        return 'pmdbm'
    return 'pmgrm'


for elem in res:
    coords.append([','.join(list(map(str, elem['geometry']['coordinates']))), get_type_point(elem)])
response = get_staticmap(toponym_coodrinates, coords)
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))

screen.blit(pygame.image.load(map_file), (0, 0))

pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()
