import pygame
from .config import BLACK, WHITE
from .ui import start_game, game_setup, ship_placement_screen
from .player import Player

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = "START_SCREEN"  # Initial game state
        self.num_ships = 0
        self.player1 = None
        self.player2 = None

    def run(self):
        # Start with the start screen
        start_game(self.screen)
        self.state = "GAME_SETUP"  # Transition to the game setup state

        # Game setup
        self.num_ships, player1_name, player2_name = game_setup(self.screen)
        self.player1 = Player(player1_name, self.num_ships)
        self.player2 = Player(player2_name, self.num_ships)
        self.state = "SHIP_PLACEMENT"  # Transition to the ship placement state

        # Ship placement
        ship_placement_screen(self.num_ships, self.player1, self.player2)
        self.state = "MAIN_GAME"  # Transition to the main game state