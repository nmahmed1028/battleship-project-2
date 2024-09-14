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

    def update(self):
        # Update the game state
        if self.state == "MAIN_GAME":
            # Update main game state
            pass

    def render(self):
        # Render the game elements based on the current state
        if self.state == "START_SCREEN":
            self.render_start_screen()
        elif self.state == "GAME_SETUP":
            self.render_game_setup()
        elif self.state == "SHIP_PLACEMENT":
            self.render_ship_placement()
        elif self.state == "MAIN_GAME":
            self.render_main_game()

    def render_start_screen(self):
            # Render the start screen elements
            font = pygame.font.Font(None, 36)
            text = font.render("Press Enter to Start", True, BLACK)
            self.screen.blit(text, (200, 300))

    def render_game_setup(self):
        # Render the game setup screen elements
        game_setup(self.screen)

    def render_ship_placement(self):
        # Render the ship placement screen elements
        ship_placement_screen(self.num_ships, self.player1.getName(), self.player2.getName())

    def render_main_game(self):
        # Render the main game elements
        font = pygame.font.Font(None, 36)
        text = font.render("Battleship Game Placeholder", True, BLACK)
        self.screen.blit(text, (200, 300))

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