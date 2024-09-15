import pygame
import sys
from .board import Board
from .player import Player
from .config import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, ROWS, COLS, WHITE, BLACK, RED, GREEN, BLUE, GRAY, DARK_GRAY, PLAYER_BOARD_OFFSET_X, OPPONENT_BOARD_OFFSET_X, BOARD_OFFSET_Y, BUTTON_RECT
from .ui import switch_player_screen


# Define Attack class
class Attack:
    def __init__(self, screen):
        self.screen = screen
        self.cell_size = CELL_SIZE
        self.button_rect = BUTTON_RECT

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

    def draw_button(self):
        """Draw the Next button."""
        pygame.draw.rect(self.screen, GREEN, self.button_rect)
        font = pygame.font.SysFont(None, 24)
        text = font.render('Next', True, BLACK)
        self.screen.blit(text, (self.button_rect.x + 20, self.button_rect.y + 15))

    def attack(self, attacker: Player, defender: Player):
        """Main attack loop where one player attacks the other."""

        # Main attack loop
        while True:
            self.screen.fill(WHITE)

            # Draw both boards
            self.draw_grid(attacker.board, PLAYER_BOARD_OFFSET_X, BOARD_OFFSET_Y)
            self.draw_grid(defender.board, OPPONENT_BOARD_OFFSET_X, BOARD_OFFSET_Y, hide_ships=True)

            # Draw the Next Button
            self.draw_button()

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
                        print("Hit! You get another turn.")
                        return True
                    else:
                        print("Miss! Turn over.")
                        return False  # End attack, no hit

            pygame.display.update()

    def attack_simulation(self, player1: Player, player2: Player) -> Player:
        player1_won = False
        player2_won = False

        while not (player1_won or player2_won):
            # Player 1's turn to attack Player 2
            player1_turn = True
            while(player1_turn):
                player1_turn = self.attack(player1, player2)
                player1_won = not player2.board.hasUnsunkShips()
                if(player1_won):
                    break
        
            switch_player_screen(self.screen)

            # Player 2's turn to attack Player 1
            player2_turn = True
            while(player2_turn):
                player2_turn = self.attack(player2, player1)
                player2_won = not player1.board.hasUnsunkShips()
                if(player2_won):
                    break

        return player1 if player1_won else player2
        

        

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
