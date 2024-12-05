import pygame
from pathlib import Path
from game.constants import FPS
from game.entities.Player import Player


class Game:
    def __init__(self, screen: pygame.display):
        self.running = True
        self.screen = screen
        self.entities = []
        # TODO: self.map = Map()
        player_sprite_path = Path(__file__).parent.parent / 'assets' / 'player' / 'player.png'
        self.player = Player(100, 100, 48, 48, sprite_path=player_sprite_path)

    def run(self):
        while self.running:
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
            self.player.move_left()
        if pressed_keys[pygame.K_d]:
            self.player.move_right()







