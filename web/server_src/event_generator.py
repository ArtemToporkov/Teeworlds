import random
import time
from os.path import join

from game_src.constants import ASSETS_PATH, MAP_WIDTH, MAP_HEIGHT, WINDOW_HEIGHT
from game_src.entities.guns.bullets import BlowingBullet
from geometry.vector import Vector


class SwitchObject:
    def __init__(self):
        self.enabled = True

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False


class EventGenerator(SwitchObject):
    def __init__(self, entities_to_send):
        super().__init__()
        self.entities_to_send = entities_to_send
        self.running = True

    def start_event(self):
        while self.running:
            if self.enabled:
                print('a')
                for _ in range(6):
                    time.sleep(random.randint(0, 2))
                    # x = random.gauss(mu=MAP_WIDTH // 2, sigma=50)
                    x = random.randint(0, MAP_WIDTH)
                    y = -100
                    size = random.randint(50, 150)
                    bomb = BlowingBullet(
                        x, y, size, size, 150, join(ASSETS_PATH, "weapons", "bullets", "bomb.png")
                    )
                    bomb.radius = 350
                    bomb.velocity = Vector(random.randint(-5, 5), 10)
                    bomb.direction = bomb.velocity.normalize()
                    time.sleep(0.1)
                    for arr in self.entities_to_send.values():
                        print('append bomb')
                        arr.append(bomb.to_dict())
            time.sleep(5 + random.randint(0, 5))
