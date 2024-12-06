from game.game import Game
from pygame import display

if __name__ == '__main__':
    screen = display.set_mode((640, 480))
    game = Game(screen)
    game.run()
