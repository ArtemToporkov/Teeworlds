import pygame
from pathlib import Path
from game.constants import FPS, BACKGROUND_WIDTH, BACKGROUND_HEIGHT, MOVEMENT_SPEED, HITBOXES_MODE
from game.entities.game_object import GameObject
from game.entities.map.map import Map
from game.entities.map.platform import Platform
from game.entities.player import Player
from game.enums import PlayerStates


class Game:
    def __init__(self, screen: pygame.display):
        self.running = True
        self.screen = screen
        # bg_path = Path(__file__).parent.parent / 'assets' / 'background.png'
        # self.background = pygame.transform.scale(pygame.image.load(bg_path), (BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
        self.clock = pygame.time.Clock()  # для фпс
        self.entities = []
        self.bullets = []
        self.players = dict()
        self.map = Map()
        self.player = Player(100,  100, 48, 48)
        self.entities = [self.player, *self.map.platforms]

    def run(self) -> None:
        while self.running:
            self.draw()
            self.process_controls(pygame.event.get())
            self.interact_entities(self.player, *self.players.values(), *self.bullets, *self.map.platforms)
            self.update_entities()
            pygame.display.flip()
            self.clock.tick(FPS)

    def interact_entities(self, *entities: GameObject) -> None:
        for first in entities:
            for second in entities:
                first.act(second)
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
                    # if MULTIPLAYER:
                    #     for bullet in bullets:
                    #         self.network.send(Wrap(bullet))
                    self.bullets.extend(bullets)

                elif event.button == 3:  # ПКМ
                    self.player.current_weapon = (self.player.current_weapon + 1) % len(self.player.weapons)

        pressed_keys = pygame.key.get_pressed()
        self.player.process_keys_and_move(pressed_keys, self.map.platforms)

    def draw(self) -> None:
        self.screen.fill((0, 0, 0))
        self.map.draw(self.screen, self.player)
        map_objects = [*self.players.values(), self.player, *self.bullets]
        for obj in map_objects:
            if obj is not None:
                obj.draw(self.screen, self.player)
