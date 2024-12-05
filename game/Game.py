import pygame
from pathlib import Path
from game.constants import FPS
from game.entities.Player import Player, States


class Game:
    def __init__(self, screen: pygame.display):
        self.running = True
        self.screen = screen
        self.entities = []
        # TODO: self.map = Map()
        self.player = Player(100, 100, 48, 48)

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            self.player.draw(self.screen)
            self.process_controls(pygame.event.get())
            pygame.display.flip()

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







