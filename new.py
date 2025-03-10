import pygame

from support import *

toponym_to_find = " ".join(sys.argv[1:])
toponym = get_geocode_json(toponym_to_find)
toponym_coodrinates = toponym["Point"]["pos"]
spn = ','.join(map(lambda x: str(float(x) / 10),
                   get_spn(toponym['boundedBy']['Envelope']['lowerCorner'],
                           toponym['boundedBy']['Envelope']['upperCorner']).split(',')))

res = search_organization(spn, ','.join(toponym_coodrinates.split()), 'Аптека')
for elem in res:
    response = get_staticmap(toponym_coodrinates, list(map(str, elem['geometry']['coordinates'])), spn)
    print(elem['properties']['name'], ','.join(list(map(str, elem['geometry']['coordinates']))),
          elem['properties']['CompanyMetaData']['Hours']['text'],
          get_distance(list(map(float, toponym_coodrinates.split(" "))),
                       list(map(float, elem['geometry']['coordinates']))))
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
    break
