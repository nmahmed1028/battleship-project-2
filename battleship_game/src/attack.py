import pygame
import sys
from .board import Board
from .player import Player

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
cell_size = 30
grid_size = 10

# Define screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Battleship - Attack Screen")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
dark_gray = (50, 50, 50)

# Board offsets
player_board_offset_x = 400  # Right side
opponent_board_offset_x = 50  # Left side
board_offset_y = 100

# Button to switch turns
button_rect = pygame.Rect(350, 500, 100, 50)

# Define Attack class
class Attack:
    def __init__(self, screen, cell_size, button_rect):
        self.screen = screen
        self.cell_size = cell_size
        self.button_rect = button_rect

    def draw_grid(self, board: Board, offset_x: int, offset_y: int, hide_ships=False) -> None:
        """Draw a grid on the board."""
        for x in range(grid_size):
            for y in range(grid_size):
                tile = board.getTile(x, y)
                rect = pygame.Rect(offset_x + x * self.cell_size, offset_y + y * self.cell_size, self.cell_size, self.cell_size)
                
                # Default tile color
                color = blue if tile.isHit() else white
                
                # Show the ship if it's player's board and it's not hidden
                if not hide_ships and tile.getPiece():
                    color = gray
                
                # Show hit or miss
                if tile.isHit():
                    color = red if tile.getPiece() else dark_gray
                
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, black, rect, 1)  # Border

    def handle_attack(self, board: Board, pos, offset_x: int, offset_y: int):
        """Handle player's attack on the opponent's board."""
        x = (pos[0] - offset_x) // self.cell_size
        y = (pos[1] - offset_y) // self.cell_size
        if 0 <= x < grid_size and 0 <= y < grid_size:
            if not board.getTile(x, y).isHit():
                return board.hit(x, y)  # Return hit or miss result
        return False  # Invalid or already hit

    def draw_button(self):
        """Draw the Next button."""
        pygame.draw.rect(self.screen, green, self.button_rect)
        font = pygame.font.SysFont(None, 24)
        text = font.render('Next', True, black)
        self.screen.blit(text, (self.button_rect.x + 20, self.button_rect.y + 15))

    def attack(self, attacker: Player, defender: Player):
        """Main attack loop where one player attacks the other."""

        # Main attack loop
        while True:
            self.screen.fill(white)

            # Draw both boards
            self.draw_grid(attacker.board, player_board_offset_x, board_offset_y)
            self.draw_grid(defender.board, opponent_board_offset_x, board_offset_y, hide_ships=True)

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
                    hit = self.handle_attack(defender.board, event.pos, opponent_board_offset_x, board_offset_y)
                    if hit:
                        print("Hit! You get another turn.")
                        return True
                    else:
                        print("Miss! Turn over.")
                        return False  # End attack, no hit

            pygame.display.update()

        return player_won  # This would return True if the player won, False otherwise


# Example of usage inside a game loop
def game():
    # Define Players
    player1 = Player()
    player2 = Player()

    # Create the Attack class object
    attack_system = Attack(screen, cell_size, button_rect)

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
    pygame.quit()

# Start the game
game()
