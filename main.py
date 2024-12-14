from game_src.constants import WINDOW_WIDTH, WINDOW_HEIGHT
from game_src.game import Game
from pygame import display


if __name__ == '__main__':
    screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    print(f'width: {WINDOW_WIDTH}, height: {WINDOW_HEIGHT}')
    game = Game(screen)

    game.run()
