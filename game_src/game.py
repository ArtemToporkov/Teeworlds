import sys
import threading
import time
from pathlib import Path

import pygame
from game_src.constants import FPS, HITBOXES_MODE, SERVER_ADDR
from game_src.entities.guns.bullets import Bullet
from game_src.entities.map.map import Map
from game_src.entities.player import Player
from game_src.utils.serialization_tools import get_entity
from web.network import Network


MULTIPLAYER = False


class Game:
    def __init__(self, screen: pygame.display):
        self.running = True
        self.screen = screen

        self.clock = pygame.time.Clock()  # для фпс
        self.entities = []
        self.bullets = []
        self.players = dict()
        self.map = Map.load_from_file(str(Path(__file__).parent.parent / 'assets' / 'maps' / 'checking.json'))
        self.player = Player(self.map.spawn_position.x,  self.map.spawn_position.y, 48, 48)
        self.entities = [self.player, *self.map.platforms]
        if MULTIPLAYER:
            self.init_multiplayer()

    def init_multiplayer(self):
        self.network = Network(*SERVER_ADDR)
        try:
            self.id, map_data = self.network.connect()
            self.map = Map.from_dict(map_data)
        except TypeError:
            print("Server not found")
            sys.exit()

        self.multiplayer_thread = threading.Thread(target=self.receive)

    def run(self) -> None:
        if MULTIPLAYER: self.multiplayer_thread.start()

        while self.running:
            self.draw()
            self.process_controls(pygame.event.get())
            self.interact_entities(self.player, *self.players.values(), *self.bullets, *self.map.platforms)
            self.update_entities()
            pygame.display.flip()
            self.clock.tick(FPS)
            #TODO Жоско полистать тикток

    def interact_entities(self, *entities: 'GameObject') -> None:
        for first in entities:
            for second in entities:
                first.interact(second)
        if HITBOXES_MODE:
            for entity in entities:
                entity.draw_hitbox(self.screen, self.player)

    def update_entities(self) -> None:
        for player in self.players.values():
            player.update()
        self.player.set_look_direction()
        self.player.update()
        if not self.player.alive:
            self.player.position = self.map.spawn_position
            self.player.alive = True
        for bullet in self.bullets:
            bullet.update()
            if not bullet.alive:
                self.bullets.remove(bullet)

    def process_controls(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # ЛКМ
                    bullets = self.player.shoot()
                    if MULTIPLAYER:
                        for bullet in bullets:
                            self.network.send(bullet.to_dict())
                    self.bullets.extend(bullets)

                elif event.button == 3:  # ПКМ
                    self.player.current_weapon = (self.player.current_weapon + 1) % len(self.player.weapons)

        pressed_keys = pygame.key.get_pressed()
        self.player.process_keys_and_move(pressed_keys, pygame.mouse.get_pos(), self.map.platforms)

    def draw(self) -> None:
        self.screen.fill((0, 0, 0))
        self.map.draw(self.screen, self.player)
        map_objects = [*self.players.values(), self.player, *self.bullets]
        for obj in map_objects:
            if obj is not None:
                obj.draw(self.screen, self.player)

    def receive(self):
        # Тречим игроков, отправляем объект игрока, получаем других игроков и новые пули на карте
        cycle = 0
        while True:
            # if self.dead:
            #     return
            # time.sleep(50 / 1000)

            to_send = self.player.to_dict()
            to_send['id'] = self.id
            try:
                data = self.network.send(to_send)
            except Exception:
                raise

            ids = []
            for wrap in data:
                entity = get_entity(wrap)

                if isinstance(entity, Player):
                    ids.append(wrap['id'])
                    if wrap['id'] not in self.players.keys():
                        self.players[wrap['id']] = entity
                    else:
                        self.players[wrap['id']].update_from_wrap(entity)
                elif isinstance(entity, Bullet):
                    self.bullets.append(entity)
                else:
                    raise ValueError

            # обновляем список игроков
            if cycle % 20 == 0:
                to_pop = []
                for key in self.players.keys():
                    if key not in ids:
                        to_pop.append(key)
                for key in to_pop:
                    self.players.pop(key)
            cycle += 1
