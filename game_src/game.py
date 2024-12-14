import asyncio
import json
import os
import sys
import threading
import time
from pathlib import Path
from asyncio import Queue

import pygame

from game_src.constants import FPS, SERVER_ADDR, ASSETS_PATH, CURRENT_LEVEL
from game_src.entities.guns.bullets import Bullet
from game_src.entities.map.map import Map
from game_src.entities.player import Player
from game_src.utils.serialization_tools import get_entity
from geometry.vector import Vector
from web.network import Network
import configparser


class Game:
    def __init__(self, screen: pygame.display):
        self.running = True
        self.screen = screen

        self.clock = pygame.time.Clock()  # для FPS
        self.entities = []
        self.bullets = []
        self.players = dict()
        self.map = Map.load_from_file(str(Path(__file__).parent.parent / 'maps' / f'{CURRENT_LEVEL}.json'))
        self.player = Player(self.map.spawn_position.x,  self.map.spawn_position.y, 48, 48)
        self.entities = [self.player, *self.map.platforms]
        self.hitboxes_mode = False

        self.input_cache = ""

        config = configparser.ConfigParser()
        config.read(str(Path(__file__).parent / 'config.ini'))
        self.multiplayer = config.getboolean("Multiplayer", "MULTIPLAYER")

        self.network = None
        self.multiplayer_thread = None

    async def init_multiplayer(self):
        network = Network(*SERVER_ADDR)
        try:
            initialize_data_from_server = await network.connect()
            self.id, map_data = initialize_data_from_server['id'], initialize_data_from_server['map']
            self.map = Map.from_dict(map_data)
            return network
        except TypeError:
            print("Server not found")
            sys.exit()

    def _run_receive_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            self.network = loop.run_until_complete(self.init_multiplayer())
            loop.run_until_complete(self.receive())
        except Exception as e:
            print(f"Error in run_receive_loop: {e}")
        finally:
            loop.close()

    def run(self) -> None:
        if self.multiplayer:
            self.multiplayer_thread = threading.Thread(target=self._run_receive_loop, daemon=True)
            self.multiplayer_thread.start()

        while self.running:
            self.draw()
            self.process_controls(pygame.event.get())
            self.interact_entities(*self.bullets, self.player, *self.players.values(), *self.map.platforms)
            self.update_entities()
            pygame.display.flip()
            self.clock.tick(FPS)
            # TODO: жоско полистать тикток

    def interact_entities(self, *entities: 'GameObject') -> None:
        for first in entities:
            for second in entities:
                first.interact(second)
        if self.hitboxes_mode:
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
            self.player.velocity = Vector(0, 0)
            self.player.move_force_vector = Vector(0, 0)
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
                    if bullets:
                        if self.multiplayer:
                            for bullet in bullets:
                                asyncio.run(self.network.send(bullet.to_dict()))
                        self.bullets.extend(bullets)

                elif event.button == 3:  # ПКМ
                    self.player.current_weapon = (self.player.current_weapon + 1) % len(self.player.weapons)

        pressed_keys = pygame.key.get_pressed()
        if not self.hitboxes_mode:
            self._check_for_cheats(pressed_keys)
        self.player.process_keys_and_move(pressed_keys, pygame.mouse.get_pos(), self.map.platforms)

    def _check_for_cheats(self, pressed_keys) -> None:
        for letter in [
            (pygame.K_s, "s"),
            (pygame.K_a, "a"),
            (pygame.K_k, "k"),
            (pygame.K_e, "e"),
            (pygame.K_v, "v"),
            (pygame.K_i, "i"),
            (pygame.K_c, "c"),
            (pygame.K_h, "h")
        ]:
            if pressed_keys[letter[0]] and (not self.input_cache or self.input_cache[-1] != letter[1]):
                self.input_cache += letter[1]
        if "sakevich" in self.input_cache:
            print("Hitboxes mode activated")
            self.hitboxes_mode = True
            self.player.hitboxes_mode = True
        if len(self.input_cache) > 50:
            self.input_cache = ""

    def draw(self) -> None:
        self.screen.fill((0, 0, 0))
        self.map.draw(self.screen, self.player)
        map_objects = [*self.players.values(), self.player, *self.bullets]
        for obj in map_objects:
            if obj is not None:
                obj.draw(self.screen, self.player)

    async def send_player_state(self):
        while True:
            to_send = self.player.to_dict()
            to_send['id'] = self.id
            try:
                await self.network.send(to_send)
            except Exception as e:
                print(f"Error sending player state: {e}")

            await asyncio.sleep(1 / FPS)

    async def process_server_messages(self):
        while True:
            try:
                data = await self.network.receive()
                if data:
                    parsed_data = json.loads(data)
                    self._process_data(parsed_data)
            except Exception as e:
                print(f"Error processing server messages: {e}")

    def _process_data(self, data):
        ids = []
        for wrap in data:
            entity = get_entity(wrap)
            if isinstance(entity, Player):
                ids.append(wrap['id'])
                if wrap['id'] not in self.players.keys():
                    # print(wrap['id'])
                    self.players[wrap['id']] = entity
                else:
                    # print(f'update: {wrap['id']}')
                    self.players[wrap['id']].update_from_wrap(entity)
            elif isinstance(entity, Bullet):
                self.bullets.append(entity)

    async def receive(self):
        await asyncio.gather(
            self.send_player_state(),
            self.process_server_messages()
        )
