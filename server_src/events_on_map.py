import random
import time
from os.path import join

from artem_lox_zatichki.entities.buff import InvisibilityBuff, SpeedBuff, JumpBuff
from artem_lox_zatichki.entities.bullets import BlowingBullet
from artem_lox_zatichki.other.constants import ROOT
from artem_lox_zatichki.other.wrapper import Wrap
from geometry.Vector import Vector


class SwitchObject:
    def __init__(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False


class BuffSpawner(SwitchObject):
    def __init__(self, game_map, entities_to_send):
        super().__init__()
        self.game_map = game_map
        self.entities_to_send = entities_to_send
        self.running = True

    def spawn_buffs(self):
        while self.running:
            if self.enabled:
                all_blocks = self.game_map.blocks.keys()
                random_blocks = random.sample(sorted(all_blocks), len(all_blocks) // 30 + 1)
                for block in random_blocks:
                    block_above = (block[0], block[1] - self.game_map.tile_size)
                    if block_above not in all_blocks:
                        buff_type = random.choice([InvisibilityBuff, SpeedBuff, JumpBuff])
                        sprite = {
                            InvisibilityBuff: join("assets", "buffs", "invisibility_buff.png"),
                            SpeedBuff: join("assets", "buffs", "speed_buff.png"),
                            JumpBuff: join("assets", "buffs", "jump_buff.png"),
                        }[buff_type]
                        buff = buff_type(
                            block_above[0],
                            block_above[1],
                            self.game_map.tile_size,
                            self.game_map.tile_size,
                            300,
                            sprite_path=sprite,
                        )
                        for arr in self.entities_to_send.values():
                            arr.append(Wrap(buff))
                        break
            time.sleep(4)


class EventGenerator(SwitchObject):
    def __init__(self, entities_to_send):
        super().__init__()
        self.entities_to_send = entities_to_send
        self.running = True

    def start_event(self):
        while self.running:
            if self.enabled:
                time.sleep(random.random() * 10 + 50)
                for _ in range(10):
                    x = random.random() * 5000
                    y = -500
                    size = random.random() * 150
                    meteor = BlowingBullet(
                        x, y, size, size, 150, join(ROOT, "assets", "bullets", "meteor.png")
                    )
                    meteor.radius = 350
                    meteor.velocity = Vector(-20, 20)
                    time.sleep(0.1)
                    for arr in self.entities_to_send.values():
                        arr.append(Wrap(meteor))
            time.sleep(5)
