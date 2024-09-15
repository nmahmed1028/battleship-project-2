import pygame
import sys
from typing import List
from ..board_mechanics.board import Board  # Import the Board class from backend
from ..board_mechanics.piece import Piece  # Import the Piece class from backend
from ..board_mechanics.player import Player
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED, GREEN, LIGHT_BLUE, FONT_NAME, FONT_SIZE

def ship_placement(screen, player: Player):
    # Set up display
    rows, cols = 10, 10  # Battleship grid is 10x10
    cell_size = 50  # Set a fixed cell size to make the grid smaller
    grid_width = cell_size * cols
    grid_height = cell_size * rows
    grid_x = (SCREEN_WIDTH - grid_width) // 2  # Center the grid horizontally
    grid_y = (SCREEN_HEIGHT - grid_height) // 2  # Center the grid vertically
    pygame.display.set_caption(f"{player.getName()}, Place Your Ships")  # Dynamic caption

    # Initialize fonts
    pygame.font.init()
    font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

    # Ship sizes (based on remaining pieces for the player)
    placed_ships = []  # Store placed ships as [(size, cells), ...]

    # Initialize backend Board for the player
    board = player.board

    # Functions
    def draw_grid():
        for x in range(grid_x, grid_x + grid_width, cell_size):
            for y in range(grid_y, grid_y + grid_height, cell_size):
                rect = pygame.Rect(x, y, cell_size, cell_size)
                pygame.draw.rect(screen, BLACK, rect, 1)

    def draw_placed_ships():
        for ship in placed_ships:
            for (x, y) in ship[1]:
                rect = pygame.Rect(grid_x + x * cell_size, grid_y + y * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, LIGHT_BLUE, rect)

    def draw_labels():
        # Draw column labels (A-J)
        for col in range(cols):
            label = font.render(chr(ord('A') + col), True, BLACK)  # Convert col index to corresponding letter
            screen.blit(label, (grid_x + col * cell_size + (cell_size - label.get_width()) // 2, grid_y - label.get_height()))

        # Draw row labels (1-10)
        for row in range(rows):
            label = font.render(str(row + 1), True, BLACK)
            screen.blit(label, (grid_x - label.get_width(), grid_y + row * cell_size + (cell_size - label.get_height()) // 2))

    def valid_placement(ship_cells):
        for (x, y) in ship_cells:
            if x < 0 or x >= cols or y < 0 or y >= rows:  # Out of bounds
                return False
            for placed_ship in placed_ships:
                if (x, y) in placed_ship[1]:  # Overlapping another ship
                    return False
        return True

    def preview_ship(mouse_pos, piece: Piece):
        grid_x_pos = (mouse_pos[0] - grid_x) // cell_size
        grid_y_pos = (mouse_pos[1] - grid_y) // cell_size

        # Calculate the cells based on the shape of the Piece
        preview_cells = [(grid_x_pos + x, grid_y_pos + y) for y, row in enumerate(piece.shape) for x, cell in enumerate(row) if cell]

        color = GREEN if valid_placement(preview_cells) else RED

        # Draw preview ship
        for (x, y) in preview_cells:
            rect = pygame.Rect(grid_x + x * cell_size, grid_y + y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, color, rect)

        return preview_cells

    # Main loop for placing ships
    current_piece = player.takeSmallestPiece()  # Get the smallest piece available
    while current_piece:
        screen.fill(WHITE)
        draw_grid()
        draw_placed_ships()
        draw_labels()  # Draw the labels for rows and columns

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Preview current ship placement based on the shape of the Piece
        current_ship_preview = preview_ship(mouse_pos, current_piece)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Rotate ship using 'R' key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    current_piece = current_piece.rotated_right()  # Rotate the piece to the right

            # Place ship on click if it's valid
            if event.type == pygame.MOUSEBUTTONDOWN:
                if valid_placement(current_ship_preview):
                    # Add ship to backend board
                    board.addPiece(current_piece, current_ship_preview[0][0], current_ship_preview[0][1])
                    placed_ships.append((current_piece.columns(), current_ship_preview))

                    # Print the board and pieces after placing
                    print("Current Board State:")
                    for row in board.grid:
                        print(['X' if tile.isHit() else ('P' if tile.getPiece() else '.') for tile in row])
                    print(f"{player.getName()} Placed Ships:", placed_ships)

                    # Get the next smallest piece
                    current_piece = player.takeSmallestPiece()

                    # Debugging: Print current piece and remaining pieces
                    print(f"Current Piece: {current_piece}")
                    print(f"Remaining Pieces: {player.unplacedPieces}")

                    # Check if no more pieces are available
                    if current_piece is None:
                        print(f"{player.getName()} has placed all ships!")
                        break

        pygame.display.update()

    print(f"{player.getName()} has placed all ships!")
