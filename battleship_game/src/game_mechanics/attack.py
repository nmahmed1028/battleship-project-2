# attack.py

"""
    The code defines an Attack class that handles player attacks on a board game, including drawing
    grids, handling attacks, displaying scores, and simulating player turns in a game loop.
    
    :param player1: Player object representing the first player in the game
    :type player1: Player
    :param player2: Player
    :type player2: Player
"""

import pygame 
import sys
import time
import random as rand
from enum import Enum
from ..board_mechanics.board import Board # Import the Board class from backend
from ..board_mechanics.player import Player # Import the Piece class from backend
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, ROWS, COLS, WHITE, BLACK, RED, GREEN, BLUE, GRAY, DARK_GRAY, PLAYER_BOARD_OFFSET_X, OPPONENT_BOARD_OFFSET_X, BOARD_OFFSET_Y, BUTTON_RECT, FONT_NAME, FONT_SIZE, TITLE_FONT_SIZE
from ..ui import switch_player_screen
from ..ai.ai import AI, HardAI, MediumAI, EasyAI
from ..ai.voice import text_to_speech

class AttackResult(Enum):
    HIT = 1
    ALREADY_HIT = 2
    MISS = 3
    INVALID = 4

# Define Attack class
# The `Attack` class in Python handles player attacks on opponent boards, manages game flow, and
# displays game elements such as grids, scores, and popup messages.
class Attack:
    def __init__(self, screen, player1: Player, player2: Player):
        # This block of code is setting up the display for the Battleship game. Here's a breakdown of what
        # each part is doing:
        # Set up display
        self.screen = screen
        self.cell_size = CELL_SIZE
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.title_font = pygame.font.SysFont(FONT_NAME, TITLE_FONT_SIZE)
        self.label_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE // 2)
        # initializing instance variables for the `Attack` object
        self.player1 = player1
        self.player2 = player2
        self.player1_score = 0 #keeping score
        self.player2_score = 0

    def draw_grid(self, board: Board, offset_x: int, offset_y: int, hide_ships=False) -> None:
        """Draw a grid on the board."""
        # This block of code is responsible for drawing the grid for the game board. Here's a
        # breakdown of what it does:
        for x in range(COLS):
            for y in range(ROWS):
                tile = board.getTile(x, y)
                rect = pygame.Rect(offset_x + x * self.cell_size, offset_y + y * self.cell_size, self.cell_size, self.cell_size)
                
                # Default tile color
                color = BLUE if tile.isHit() else WHITE
                
                # Show the ship if it's player's board and it's not hidden
                if not hide_ships and tile.getPiece():
                    color = GRAY
                
                # Show hit or miss
                if tile.isHit():
                    color = RED if tile.getPiece() else DARK_GRAY
                
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 1)  # Border
        

        for x in range(COLS):
            col_label = chr(ord('A') + x)  # Convert x to letter (A, B, C,...)
            self.draw_text(col_label, offset_x + (x + 0.5) * self.cell_size, offset_y - 10, self.label_font)

        # Draw row labels (1-10)
        for y in range(ROWS):
            row_label = str(y + 1)  # Convert y to number (1, 2, 3,...)
            self.draw_text(row_label, offset_x - 20, offset_y + (y + 0.5) * self.cell_size, self.label_font)

    def handle_attack(self, board: Board, pos, offset_x: int, offset_y: int) -> AttackResult:
        """Handle player's attack on the opponent's board."""
        x = (pos[0] - offset_x) // self.cell_size
        y = (pos[1] - offset_y) // self.cell_size
        if 0 <= x < COLS and 0 <= y < ROWS:
            if not board.getTile(x, y).isHit():
                res = board.hit(x, y)  # Return hit or miss result
                if res:
                    return AttackResult.HIT
                else:
                    return AttackResult.MISS
            else:
                return AttackResult.ALREADY_HIT
        else:
            return AttackResult.INVALID

    def draw_text(self, text, x, y, font, color=BLACK) -> None:
        """Draw text on the screen."""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def draw_scores(self) -> None:
        """Draw the scores for both players."""
        self.draw_text(f"{self.player1.getName()}: {self.player1_score}", 100, SCREEN_HEIGHT - 30, self.font)
        self.draw_text(f"{self.player2.getName()}: {self.player2_score}", SCREEN_WIDTH - 100, SCREEN_HEIGHT - 30, self.font)

    def attack_ai(self, attacker: AI, defender: Player) -> bool:
        """Handle AI's attack on the opponent's board."""
        self.screen.fill(WHITE)

        # Draw both boards
        self.draw_grid(defender.board, PLAYER_BOARD_OFFSET_X, BOARD_OFFSET_Y)
        self.draw_grid(attacker.board, OPPONENT_BOARD_OFFSET_X, BOARD_OFFSET_Y, hide_ships=True)

        # Draw labels
        self.draw_text("Your Hits", PLAYER_BOARD_OFFSET_X + (COLS * CELL_SIZE) // 2, BOARD_OFFSET_Y - 30, self.font)
        self.draw_text("Your Attacks", OPPONENT_BOARD_OFFSET_X + (COLS * CELL_SIZE) // 2, BOARD_OFFSET_Y - 30, self.font)

        self.draw_text(f"{attacker.getName()}'s Turn", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, self.title_font)

        # Draw scores
        self.draw_scores()

        pygame.display.update()
        time.sleep(0.25)

        if isinstance(attacker, HardAI):
            attacker.update_targets(defender.board)
        x, y = attacker.attack_pattern(defender.board)
        hit = self.handle_attack(defender.board, (x * self.cell_size + OPPONENT_BOARD_OFFSET_X, y * self.cell_size + BOARD_OFFSET_Y), OPPONENT_BOARD_OFFSET_X, BOARD_OFFSET_Y)
        self.draw_grid(defender.board, PLAYER_BOARD_OFFSET_X, BOARD_OFFSET_Y)
        self.draw_grid(attacker.board, OPPONENT_BOARD_OFFSET_X, BOARD_OFFSET_Y, hide_ships=True)
        if hit == AttackResult.HIT:
            if isinstance(attacker, MediumAI):
                if attacker.last_hits is None:
                    attacker.last_hits = [(x, y, True)]
                else:
                    attacker.last_hits.append((x, y, True))
                # check if ships sunk
                if defender.board.getTile(x, y).getPiece().isSunk():
                    attacker.last_hits = None
            self.show_popup("AI hit", 1)
            if defender.board.getTile(x, y).getPiece().isSunk(): # Same as checking hits for med, but applies dialogue for all AI
                self.show_dialogue_sink(attacker, 0.5) # Ship sink dialogue
            else: 
                self.show_dialogue_hit(attacker, 0.5) # Ship hit dialogue
            if attacker is self.player1:
                self.player1_score += 1
            else:
                self.player2_score += 1
            return True
        else:
            if isinstance(attacker, MediumAI):
                if attacker.last_hits is not None:
                    attacker.last_hits.append((x, y, False))
            self.show_popup("AI miss", 1)
            self.show_dialogue_miss(attacker, 0.5) # Miss dialogue
            return False

    def attack(self, attacker: Player, defender: Player)  -> bool:
        """Main attack loop where one player attacks the other."""

        # Main attack loop
        while True:
            self.screen.fill(WHITE)

            # Draw both boards
            self.draw_grid(attacker.board, PLAYER_BOARD_OFFSET_X, BOARD_OFFSET_Y)
            self.draw_grid(defender.board, OPPONENT_BOARD_OFFSET_X, BOARD_OFFSET_Y, hide_ships=True)


            # Draw labels
            self.draw_text("Your Hits", PLAYER_BOARD_OFFSET_X + (COLS * CELL_SIZE) // 2, BOARD_OFFSET_Y - 30, self.font)
            self.draw_text("Your Attacks", OPPONENT_BOARD_OFFSET_X + (COLS * CELL_SIZE) // 2, BOARD_OFFSET_Y - 30, self.font)

            self.draw_text(f"{attacker.getName()}'s Turn", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, self.title_font)

            # Draw scores
            self.draw_scores()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Handle mouse clicks (attack)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Attack opponent's board
                    hit = self.handle_attack(defender.board, event.pos, OPPONENT_BOARD_OFFSET_X, BOARD_OFFSET_Y)
                    self.draw_grid(defender.board, OPPONENT_BOARD_OFFSET_X, BOARD_OFFSET_Y, hide_ships=True)
                    if hit == AttackResult.HIT:
                        self.show_popup("Hit! You get another turn.", 1)
                        # update scores
                        if attacker is self.player1:
                            self.player1_score += 1
                        else:
                            self.player2_score += 1

                        return True
                    elif hit == AttackResult.MISS:
                        self.show_popup("Miss! Turn over.", 1)
                        return False  # End attack, no hit
                    elif hit == AttackResult.ALREADY_HIT:
                        print("Already hit!")
                    elif hit == AttackResult.INVALID:
                        print("Invalid attack!")

            pygame.display.update()

    def show_popup(self, message, duration)  -> None:
        """Show a temporary popup message."""
        self.draw_text(message, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, self.font, RED)
        pygame.display.update()
        time.sleep(duration)

    def show_dialogue(self, attacker, dialogue) -> None:
        if isinstance(attacker, HardAI):
            text_to_speech(dialogue, "com.apple.speech.synthesis.voice.Hysterical", 3000)
        elif isinstance(attacker, MediumAI):
            text_to_speech(dialogue, "com.apple.voice.compact.en-IE.Moira")
        else: # Easy AI
            text_to_speech(dialogue, "com.apple.speech.synthesis.voice.Junior")

    def show_dialogue_hit(self, attacker: AI, duration)  -> None:
        """Show a temporary popup message."""
        dialogue = attacker.dialogue_hit[rand.randrange(0,len(attacker.dialogue_hit))]
        message = "AI: \""
        message += dialogue
        message += "\""
        self.draw_text(message, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 135, self.font, DARK_GRAY)
        pygame.display.update()
        self.show_dialogue(attacker, dialogue)
        time.sleep(duration)

    def show_dialogue_sink(self, attacker: AI, duration) -> None:
        """Show a temporary popup message."""
        dialogue = attacker.dialogue_sink[rand.randrange(0,len(attacker.dialogue_hit))]
        message = "AI: \""
        message += dialogue
        message += "\""
        self.draw_text(message, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 135, self.font, DARK_GRAY)
        pygame.display.update()
        self.show_dialogue(attacker, dialogue)
        time.sleep(duration)
    
    def show_dialogue_miss(self, attacker: AI, duration) -> None:
        """Show a temporary popup message."""
        dialogue = attacker.dialogue_miss[rand.randrange(0,len(attacker.dialogue_hit))]
        message = "AI: \""
        message += dialogue
        message += "\""
        self.draw_text(message, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 135, self.font, DARK_GRAY)
        pygame.display.update()
        self.show_dialogue(attacker, dialogue)
        time.sleep(duration)

    def show_dialogue_win(self, attacker: AI, duration) -> None:
        """Show a temporary popup message."""
        dialogue = attacker.dialogue_win[rand.randrange(0,len(attacker.dialogue_hit))]
        message = "AI: \""
        message += dialogue
        message += "\""
        self.draw_text(message, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, self.font, RED)
        pygame.display.update()
        self.show_dialogue(attacker, dialogue)
        time.sleep(duration)

    def show_dialogue_lose(self, attacker: AI, duration) -> None:
        """Show a temporary popup message."""
        dialogue = attacker.dialogue_lose[rand.randrange(0,len(attacker.dialogue_hit))]
        message = "AI: \""
        message += dialogue
        message += "\""
        self.draw_text(message, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, self.font, RED)
        pygame.display.update()
        self.show_dialogue(attacker, dialogue)
        time.sleep(duration)

    def attack_simulation(self) -> Player:
        """
        The function simulates a turn-based attack game between two players until one player wins by
        sinking all of the opponent's ships.
        :return: The `attack_simulation` method returns the player who won the game, either
        `self.player1` or `self.player2`.
        """
        player1_won = False
        player2_won = False

        while not (player1_won or player2_won):
            # Player 1's turn to attack Player 2
            player1_turn = True
            while(player1_turn):
                if isinstance(self.player1, AI):
                    player1_turn = self.attack_ai(self.player1, self.player2)
                else:
                    player1_turn = self.attack(self.player1, self.player2)
                player1_won = not self.player2.board.hasUnsunkShips()
                if(player1_won):
                    break
        
            if player1_won:
                if isinstance(self.player2, AI): # Shows dialogue for when AI loses
                    self.show_dialogue_lose(self.player2,1)
                break
            if not isinstance(self.player2, AI):
                switch_player_screen(self.screen)

            # Player 2's turn to attack Player 1
            player2_turn = True
            while(player2_turn):
                if isinstance(self.player2, AI):
                    player2_turn = self.attack_ai(self.player2, self.player1)
                else:
                    player2_turn = self.attack(self.player2, self.player1)
                player2_won = not self.player1.board.hasUnsunkShips()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                if(player2_won):
                    break
            
            if player2_won:
                if isinstance(self.player2, AI): # Shows Dialogue for when AI wins
                    self.show_dialogue_win(self.player2, 1)
                break
            if not isinstance(self.player2, AI):
                switch_player_screen(self.screen)

        return self.player1 if player1_won else self.player2
        

        

# Example of usage inside a game loop
def game(player1: Player, player2: Player)  -> None:
    # Create the Attack class object
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    attack_system = Attack(screen)

    # Place some ships (for demo purposes)
    player1.board.addPiece(player1.unplacedPieces[0], 1, 1)  # Manually place a ship on player's board
    player2.board.addPiece(player2.unplacedPieces[0], 3, 3)  # Manually place a ship on opponent's board

    player1_won = False
    player2_won = False

    while not (player1_won or player2_won):
        # Player 1's turn to attack Player 2
        # player's turn in the game loop.
        player1_turn = True
        while(player1_turn):
            player1_turn = attack_system.attack(player1, player2)
            player1_won = not player2.board.hasUnsunkShips()
            if(player1_won):
                break
        # Transition screen can go here if needed
        
        # Player 2's turn to attack Player 1
        player2_turn = True
        while(player2_turn):
            player2_turn = attack_system.attack(player2, player1)
            player2_won = not player1.board.hasUnsunkShips()
            if(player2_won):
                break
        
        

        # Transition screen can go here if needed
    if player1_won:
            print("Player 1 won!")

    if player2_won:
            print("Player 2 won!")
