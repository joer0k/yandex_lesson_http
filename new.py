from support import *

toponym_to_find = " ".join(sys.argv[1:])
toponym = get_geocode_json(toponym_to_find)
toponym_coodrinates = toponym["Point"]["pos"]

print(get_district(toponym_coodrinates)['name'])