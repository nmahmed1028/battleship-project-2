# main.py
"""
main.py

This module initializes and runs the Battleship game using Pygame.

Functions:
    main(): Initializes Pygame, sets up the display, creates a Game instance, and runs the game.

Usage:
    Run this module directly to start the Battleship game.
"""

import pygame
from .config import SCREEN_WIDTH, SCREEN_HEIGHT
from .game import Game
# this import is required to make relative imports work in tests
from . import tests

def main():
    """
    The `main` function initializes a Pygame window for a Battleship game and runs the initial game
    setup.
    """
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Battleship Game")

    # Create game instance
    game = Game(screen)

    # Run the initial game setup (start screen)
    game.run()

if __name__ == "__main__":
    main()