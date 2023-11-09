import pygame
import sys

from game import Game


def main():
    pygame.init()
    pygame.font.init()
    game = Game()
    game.main_loop()
    sys.exit()


if __name__ == '__main__':
    main()
