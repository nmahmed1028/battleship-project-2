import pygame
import sys
import time
from ..board_mechanics.board import Board
from ..board_mechanics.player import Player
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, ROWS, COLS, WHITE, BLACK, RED, GREEN, BLUE, GRAY, DARK_GRAY, PLAYER_BOARD_OFFSET_X, OPPONENT_BOARD_OFFSET_X, BOARD_OFFSET_Y, BUTTON_RECT, FONT_NAME, FONT_SIZE, TITLE_FONT_SIZE
from ..ui import switch_player_screen


# Define Attack class
class Attack:
    def __init__(self, screen, player1: Player, player2: Player):
        self.screen = screen
        self.cell_size = CELL_SIZE
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.title_font = pygame.font.SysFont(FONT_NAME, TITLE_FONT_SIZE)
        self.player1 = player1
        self.player2 = player2
        self.player1_score = 0
        self.player2_score = 0

    def draw_grid(self, board: Board, offset_x: int, offset_y: int, hide_ships=False) -> None:
        """Draw a grid on the board."""
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

    def handle_attack(self, board: Board, pos, offset_x: int, offset_y: int):
        """Handle player's attack on the opponent's board."""
        x = (pos[0] - offset_x) // self.cell_size
        y = (pos[1] - offset_y) // self.cell_size
        if 0 <= x < COLS and 0 <= y < ROWS:
            if not board.getTile(x, y).isHit():
                return board.hit(x, y)  # Return hit or miss result
        return False  # Invalid or already hit

    def draw_text(self, text, x, y, font, color=BLACK):
        """Draw text on the screen."""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def draw_scores(self):
        """Draw the scores for both players."""
        self.draw_text(f"{self.player1.getName()}: {self.player1_score}", 100, SCREEN_HEIGHT - 30, self.font)
        self.draw_text(f"{self.player2.getName()}: {self.player2_score}", SCREEN_WIDTH - 100, SCREEN_HEIGHT - 30, self.font)

    def attack(self, attacker: Player, defender: Player):
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
                    if hit:
                        self.show_popup("Hit! You get another turn.", 1)
                        # update scores
                        if attacker is self.player1:
                            self.player1_score += 1
                        else:
                            self.player2_score += 1

                        return True
                    else:
                        self.show_popup("Miss! Turn over.", 1)
                        return False  # End attack, no hit

            pygame.display.update()

    def show_popup(self, message, duration):
        """Show a temporary popup message."""
        self.draw_text(message, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, self.font, RED)
        pygame.display.update()
        time.sleep(duration)

    def attack_simulation(self) -> Player:
        player1_won = False
        player2_won = False

        while not (player1_won or player2_won):
            # Player 1's turn to attack Player 2
            player1_turn = True
            while(player1_turn):
                player1_turn = self.attack(self.player1, self.player2)
                player1_won = not self.player2.board.hasUnsunkShips()
                if(player1_won):
                    break
        
            switch_player_screen(self.screen)

            # Player 2's turn to attack Player 1
            player2_turn = True
            while(player2_turn):
                player2_turn = self.attack(self.player2, self.player1)
                player2_won = not self.player1.board.hasUnsunkShips()
                if(player2_won):
                    break

        return self.player1 if player1_won else self.player2
        

        

# Example of usage inside a game loop
def game(player1: Player, player2: Player):
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