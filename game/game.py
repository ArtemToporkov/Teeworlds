import pygame
from pathlib import Path
from game.constants import FPS, BACKGROUND_WIDTH, BACKGROUND_HEIGHT, MOVEMENT_SPEED, HITBOXES_MODE
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
        self.entities = [self.player, *self.map.blocks.values()]

    def run(self):
        while self.running:
            self.draw()
            self.process_controls(pygame.event.get())
            # self.check_collisions([self.player])
            # self.check_collisions(self.players.values())
            self.act_entities(
                self.player, *self.players.values(), *self.bullets, #*self.buffs
            )
            self.check_collisions(self.bullets)
            self.update_entities()
            pygame.display.flip()
            self.clock.tick(FPS)

    def act_entities(self, *entities):
        for first in entities:
            for second in entities:
                first.act(second)

    def check_collisions(self, entities):
        for entity in entities:
            entity.collide(self.map)

    def update_entities(self):
        for player in self.players.values():
            player.update()
        self.player.set_direction()
        self.player.update()
        if not self.player.alive:
            self.player.position = self.map.spawn_position
            self.player.alive = True
        for bullet in self.bullets:
            bullet.update()
            if not bullet.alive:
                self.bullets.remove(bullet)
        # for buff in self.buffs:
        #     if not buff.alive:
        #         self.buffs.remove(buff)
        # if self.hook is not None:
        #     self.hook.update()

    def process_controls(self, events: list[pygame.event.Event]):
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
                    for bullet in bullets:
                        self.bullets.append(bullet)

                elif event.button == 3:  # ПКМ
                    self.player.current_weapon = (self.player.current_weapon + 1) % len(self.player.weapons)

        pressed_keys = pygame.key.get_pressed()
        self.player.process_keys_and_move(pressed_keys, self.map.blocks.values())
        for entity in self.entities:
            if HITBOXES_MODE:
                entity.draw_hitbox(self.screen, self.player.position)
            for e in self.entities:
                e.interact(entity)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.map.draw(self.screen, self.player.position)

        map_objects = [*self.players.values(), self.player, *self.bullets]  # *self.buffs]

        for obj in map_objects:
            if obj is not None:
                obj.draw(self.screen, self.player.position)

        if HITBOXES_MODE:
            new_position = self.player.get_coordinates_offset_by_center(self.player.position)
            pygame.draw.circle(self.screen, (0, 255, 0), (new_position.x, new_position.y), 5)
