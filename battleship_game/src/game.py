# game.py
"""
This module contains the Game class which manages the overall flow of the Battleship game.

Classes:
    Game: Manages the game states and transitions between different phases of the game.

Methods:
    __init__(screen):
        Initializes the Game object with the given screen.
        
    run():
        Runs the game by transitioning through various states such as start screen, game setup, ship placement, main game, and end game.
"""


# The `import` statements at the beginning of the code are used to bring in functionality from other
# modules or packages. Here's what each import statement is doing:
import pygame
from .config import BLACK, WHITE
from .ui import start_game, game_setup, switch_player_screen, end_game, select_game_mode, select_ai_difficulty, single_player_setup
from .board_mechanics.player import Player
from .game_mechanics.place_ships import ship_placement
from .game_mechanics.attack import Attack
from .ai.ai import AI, EasyAI, MediumAI, HardAI

class Game:
    def __init__(self, screen):
        """
        The function initializes game state variables and player information for a game screen.
        
        :param screen: The `screen` parameter in the `__init__` method is typically used to store a
        reference to the screen or display surface where the game will be rendered. This allows the game
        objects to interact with and be displayed on the screen. It is a common practice in game
        development to pass the screen
        """
        self.screen = screen
        self.state = "START_SCREEN"  # Initial game state
        self.num_ships = 0
        self.player1 = None
        self.player2 = None

    def run(self):
        """
        The function runs a turn-based battleship game with ship placement, attacks, and game over
        conditions.
        """
        # Start with the start screen
        start_game(self.screen)
        self.state = "GAME_SETUP"  # Transition to the game setup state

        game_mode = select_game_mode(self.screen) #select game mode (single or multi)
        if game_mode == "single":
            #difficulty = select_ai_difficulty(self.screen) #select ai difficulty
            self.num_ships, player_name, difficulty = single_player_setup(self.screen) #sets up human player
            self.player1 = Player(player_name, self.num_ships)

            #initialize player 2 as ai based on chosen difficulty
            if difficulty == "easy":
                self.player2 = EasyAI(self.num_ships)
            elif difficulty == "medium":
                self.player2 = MediumAI(self.num_ships)
            elif difficulty == "hard": 
                self.player2 = HardAI(self.num_ships, self.player1.board)

        else: #multiplayer setup
            self.num_ships, player1_name, player2_name = game_setup(self.screen)
            self.player1 = Player(player1_name, self.num_ships)
            self.player2 = Player(player2_name, self.num_ships)

        self.state = "SHIP_PLACEMENT"  # Transition to the ship placement state

        # Ship placement
        print(f"Placing {self.num_ships} ships for, {self.player1}, and {self.player2}")
        ship_placement(self.screen, self.player1)
        if not isinstance(self.player2, AI):
            switch_player_screen(self.screen)
        ship_placement(self.screen, self.player2)
        if not isinstance(self.player2, AI):
            switch_player_screen(self.screen)
        print("both players have placed their ships")
        self.state = "MAIN_GAME"  # Transition to the main game state
        pygame.display.set_caption("Let's Play!")  # Dynamic caption

        # Attacks
        attack_system = Attack(self.screen, self.player1, self.player2)
        winner = attack_system.attack_simulation()
        self.state = "END_GAME"
        end_game(self.screen, winner)
        self.state = "GAME_OVER"
        print("Game over")
