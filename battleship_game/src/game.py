import pygame
from .config import BLACK, WHITE
from .ui import start_game, game_setup, switch_player_screen, end_game
from .place_ships import ship_placement 
from .player import Player
from .attack import Attack

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
        print(f"Placing {self.num_ships} ships for, {self.player1}, and {self.player2}")
        ship_placement(self.screen, self.player1)
        switch_player_screen(self.screen)
        ship_placement(self.screen, self.player2)
        switch_player_screen(self.screen)
        print("both players have placed their ships")
        self.state = "MAIN_GAME"  # Transition to the main game state

        # Attacks
        attack_system = Attack(self.screen)
        winner = attack_system.attack_simulation(self.player1, self.player2)
        self.state = "END_GAME"
        end_game(self.screen, winner)
        self.state = "GAME_OVER"
        print("Game over")
