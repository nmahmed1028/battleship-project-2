# main.py

import pygame
from .config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
from .game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Battleship Game")

    # Create game instance
    game = Game(screen)

    # Run the initial game setup (start screen)
    game.run()

if __name__ == "__main__":
    main()