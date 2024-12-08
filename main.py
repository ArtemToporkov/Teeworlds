from game.constants import WINDOW_WIDTH, WINDOW_HEIGHT
from game.game import Game
from pygame import display


if __name__ == '__main__':
    screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    game = Game(screen)

    game.run()
