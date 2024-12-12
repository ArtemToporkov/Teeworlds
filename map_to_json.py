import os

from game_src.constants import ASSETS_PATH
from game_src.entities.map.map import Map
import json

map = Map()
js = json.dumps(map.to_dict(), indent=4)
with open(os.path.join(ASSETS_PATH, 'maps', 'online_map.json'), 'w') as file:
    file.write(js)
