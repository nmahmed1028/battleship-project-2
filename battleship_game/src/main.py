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

    # Main game loop
    running = True
    clock = pygame.time.Clock()

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update game state
        game.update()

        # Render everything
        screen.fill(WHITE)
        game.render()

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()