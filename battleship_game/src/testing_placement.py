import pygame
import sys
from board import Board  # Import the Board class from backend
from piece import Piece  # Import the Piece class from backend

def ship_placement():
    # Initialize Pygame
    pygame.init()

    # Set up display
    width, height = 600, 600
    rows, cols = 10, 10  # Battleship grid is 10x10
    cell_size = width // cols
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Place Your Ships")

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    blue = (0, 0, 255)
    red = (255, 0, 0)
    gray = (200, 200, 200)
    green = (0, 255, 0)

    # Ship sizes
    ship_sizes = [5, 4, 3, 2, 1]  # Sizes of ships to place
    placed_ships = []  # Store placed ships as [(size, cells), ...]

    # Currently placing ship
    placing_ship = None  # Format: (ship_size, [(x, y)] cells)
    current_ship_index = 0  # Start with first ship (5-units)
    horizontal = True  # True for horizontal, False for vertical

    # Initialize backend Board
    board = Board()

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

    def preview_ship(mouse_pos, size, horizontal):
        grid_x = mouse_pos[0] // cell_size
        grid_y = mouse_pos[1] // cell_size
        preview_cells = [(grid_x + i if horizontal else grid_x, grid_y if horizontal else grid_y + i) for i in range(size)]
        color = green if valid_placement(preview_cells) else red

        # Draw preview ship
        for (x, y) in preview_cells:
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, color, rect)

        return preview_cells

    # Main loop for placing ships
    while current_ship_index < len(ship_sizes):
        screen.fill(white)
        draw_grid()
        draw_placed_ships()

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Preview current ship placement
        current_ship_size = ship_sizes[current_ship_index]
        current_ship_preview = preview_ship(mouse_pos, current_ship_size, horizontal)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Toggle ship orientation (horizontal/vertical) with 'R' key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    horizontal = not horizontal

            # Place ship on click if it's valid
            if event.type == pygame.MOUSEBUTTONDOWN:
                if valid_placement(current_ship_preview):
                    # Create a piece based on the shape defined above
                    piece_shape = [[True] * current_ship_size] if horizontal else [[True] for _ in range(current_ship_size)]
                    piece = Piece(piece_shape)  # Pass the shape directly

                    # Add ship to backend board
                    print("Placing ship of size", current_ship_size, "at", current_ship_preview[0][0], "and", current_ship_preview[0][1])
                    board.addPiece(piece, current_ship_preview[0][0], current_ship_preview[0][1])
                    placed_ships.append((current_ship_size, current_ship_preview))
                    current_ship_index += 1  # Move to the next ship

                    # Print the board and pieces after placing
                    print("Current Board State:")
                    for row in board.grid:
                        print(['X' if tile.isHit() else ('P' if tile.getPiece() else '.') for tile in row])
                    print("Placed Ships:", placed_ships)

        pygame.display.update()

    # When all ships are placed, transition to the main game (battleship guessing screen)
    pygame.quit()
    print("All ships placed! Transitioning to the main game...")
