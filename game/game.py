import pygame
from pathlib import Path
from game.constants import FPS, BACKGROUND_WIDTH, BACKGROUND_HEIGHT
from game.entities.map.map import Map
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
        self.player = Player(100, 250, 48, 48)

    def run(self):
        while self.running:
            self.draw()
            self.process_controls(pygame.event.get())
            self.check_collisions([self.player])

            self.check_collisions(self.bullets)
            self.check_collisions(self.players.values())
            self.update_entities()
            pygame.display.flip()
            self.clock.tick(FPS)


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

        # for particle in self.particles:
        #     particle.update()
        #     if not particle.alive:
        #         self.particles.remove(particle)

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
                        bullet.load_images()

                elif event.button == 3:  # ПКМ
                    self.player.current_weapon = (self.player.current_weapon + 1) % len(self.player.weapons)

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_a]:
            self.player.state = PlayerStates.RUNNING_LEFT
            self.player.move_left()
        elif pressed_keys[pygame.K_d]:
            self.player.state = PlayerStates.RUNNING_RIGHT
            self.player.move_right()
        # TODO: elif pressed_keys[pygame.K_w]: ...
        else:
            self.player.state = PlayerStates.STANDING

    def draw(self):
        self.map.draw(self.screen, self.player.position)
        self.player.draw(self.screen)







