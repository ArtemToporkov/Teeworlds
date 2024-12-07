import pygame
from pathlib import Path
from game.constants import FPS, BACKGROUND_WIDTH, BACKGROUND_HEIGHT, HITBOXES_MODE, MOVEMENT_SPEED
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
        self.map = Map()
        self.player = Player(100,  100, 48, 48)
        self.entities = [self.player, *self.map.blocks.values()]

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
            self.player.state = PlayerStates.RUNNING_LEFT
            self.player.change_move_vector(x=-MOVEMENT_SPEED)
        elif pressed_keys[pygame.K_d]:
            self.player.state = PlayerStates.RUNNING_RIGHT
            self.player.change_move_vector(x=MOVEMENT_SPEED)
        elif pressed_keys[pygame.K_w]:
            if not self.player.jumped:
                self.player.jumped = True
                self.player.change_move_vector(y=-2*MOVEMENT_SPEED)
        else:
            self.player.state = PlayerStates.STANDING
        self.player.move()
        for entity in self.entities:
            if HITBOXES_MODE:
                entity.draw_hitbox(self.screen)
            for e in self.entities:
                e.intersects(entity)
                if isinstance(e, Platform):
                    e.interact(entity)

    def draw(self):
        self.map.draw(self.screen, self.player.position)
        self.player.draw(self.screen, self.player.position)
        new_position = self.player.get_coordinates_offset_by_center(self.player.position)
        if HITBOXES_MODE:
            pygame.draw.circle(self.screen, (0, 255, 0), (new_position.x, new_position.y), 5)








