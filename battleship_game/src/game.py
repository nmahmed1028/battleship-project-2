# game.py

import pygame
from .config import BLACK, WHITE
from .ui import start_game

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = "START_SCREEN"  # Initial game state

    def update(self):
        # Update the game state
        if self.state == "MAIN_GAME":
            # Update main game state
            pass

    def render(self):
        # Render the game elements based on the current state
        if self.state == "START_SCREEN":
            self.render_start_screen()
        elif self.state == "MAIN_GAME":
            self.render_main_game()

    def render_start_screen(self):
        # Render the start screen elements
        font = pygame.font.Font(None, 36)
        text = font.render("Press Enter to Start", True, BLACK)
        self.screen.blit(text, (200, 300))

    def render_main_game(self):
        # Render the main game elements
        font = pygame.font.Font(None, 36)
        text = font.render("Battleship Game Placeholder", True, BLACK)
        self.screen.blit(text, (200, 300))

    def run(self):
        start_game(self.screen)
        self.state = "MAIN_GAME"  # Transition to the main game state