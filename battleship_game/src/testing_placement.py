import pygame
import sys
from typing import List
from board import Board  # Import the Board class from backend
from piece import Piece  # Import the Piece class from backend
from player import Player
def ship_placement(player: Player):
    # Initialize Pygame
    pygame.init()

    # Set up display
    width, height = 600, 600
    rows, cols = 10, 10  # Battleship grid is 10x10
    cell_size = width // cols
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(f"{player.getName()}, Place Your Ships")  # Dynamic caption

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    gray = (200, 200, 200)
    green = (0, 255, 0)

    # Ship sizes (based on remaining pieces for the player)
    placed_ships = []  # Store placed ships as [(size, cells), ...]

    # Initialize backend Board for the player
    board = player.board

    # Functions
    def draw_grid():
        for x in range(0, width, cell_size):
            for y in range(0, height, cell_size):
                rect = pygame.Rect(x, y, cell_size, cell_size)
                pygame.draw.rect(screen, black, rect, 1)

    def draw_placed_ships():
        for ship in placed_ships:
            for (x, y) in ship[1]:
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, gray, rect)

    def valid_placement(ship_cells):
        for (x, y) in ship_cells:
            if x < 0 or x >= cols or y < 0 or y >= rows:  # Out of bounds
                return False
            for placed_ship in placed_ships:
                if (x, y) in placed_ship[1]:  # Overlapping another ship
                    return False
        return True

    def preview_ship(mouse_pos, piece: Piece):
        grid_x = mouse_pos[0] // cell_size
        grid_y = mouse_pos[1] // cell_size

        # Calculate the cells based on the shape of the Piece
        preview_cells = [(grid_x + x, grid_y + y) for y, row in enumerate(piece.shape) for x, cell in enumerate(row) if cell]

        color = green if valid_placement(preview_cells) else red

        # Draw preview ship
        for (x, y) in preview_cells:
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, color, rect)

        return preview_cells

    # Main loop for placing ships
    current_piece = player.takeSmallestPiece()  # Get the smallest piece available
    while current_piece:
        screen.fill(white)
        draw_grid()
        draw_placed_ships()

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

    pygame.quit()
    print(f"{player.getName()} has placed all ships!")
