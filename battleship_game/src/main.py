# main.py
"""
main.py

This module initializes and runs the Battleship game using Pygame.

Functions:
    main(): Initializes Pygame, sets up the display, creates a Game instance, and runs the game.

Usage:
    Run this module directly to start the Battleship game.
"""

import asyncio
from threading import Thread
import pygame
from .config import SCREEN_WIDTH, SCREEN_HEIGHT
from .game import Game
# this import is required to make relative imports work in tests
from . import tests
from .ai.voice import init_voice_engine

loop = asyncio.new_event_loop()
running = True
def side_thread(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

thread = Thread(target=side_thread, args=(loop,), daemon=True)
thread.start()

async def main():
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
    future = asyncio.run_coroutine_threadsafe(init_voice_engine(), loop)
    game.run(future, loop)

if __name__ == "__main__":
    asyncio.run(main())
