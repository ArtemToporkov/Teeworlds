import pygame
from pathlib import Path
from game.constants import FPS, BACKGROUND_WIDTH, BACKGROUND_HEIGHT
from game.entities.player import Player, States
from game.entities.map.map import Map


class Game:
    def __init__(self, screen: pygame.display):
        self.running = True
        self.screen = screen
        # bg_path = Path(__file__).parent.parent / 'assets' / 'background.png'
        # self.background = pygame.transform.scale(pygame.image.load(bg_path), (BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
        self.clock = pygame.time.Clock()  # для фпс
        self.entities = []
        self.map = Map()
        self.player = Player(100, 100, 48, 48)

    def run(self):
        while self.running:
            self.draw()
            self.process_controls(pygame.event.get())
            pygame.display.flip()
            self.clock.tick(FPS)

    def process_controls(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                quit()
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_a]:
            self.player.state = States.RUNNING_LEFT
            self.player.move_left()
        elif pressed_keys[pygame.K_d]:
            self.player.state = States.RUNNING_RIGHT
            self.player.move_right()
        # TODO:
        # elif pressed_keys[pygame.K_w]:
        #   self.player.jump()
        else:
            self.player.state = States.STANDING

    def draw(self):
        self.map.draw(self.screen, self.player.position)
        self.player.draw(self.screen)







