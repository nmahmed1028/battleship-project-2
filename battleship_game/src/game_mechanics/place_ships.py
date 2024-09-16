import pygame
import sys
from typing import List
from ..board_mechanics.board import Board  # Import the Board class from backend
from ..board_mechanics.piece import Piece  # Import the Piece class from backend
from ..board_mechanics.player import Player
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED, GREEN, LIGHT_BLUE, FONT_NAME, FONT_SIZE


    """
    The function `ship_placement` allows a player to interactively place their ships on a grid while
    providing visual feedback and ensuring valid placements.
    
    :param screen: The `screen` parameter in the `ship_placement` function represents the Pygame display
    surface where the game interface will be drawn. It is the window where all the graphics, including
    the grid, ships, labels, and interactions, will be displayed to the player. The `screen` parameter
    is passed
    :param player: The `player` parameter in the `ship_placement` function represents a player object in
    a Battleship game. This player object contains information about the player, such as their name,
    remaining ships, and their game board configuration. The player object likely has methods to
    interact with the game, such as placing
    :type player: Player
    """

def ship_placement(screen, player: Player) -> None:
    # This block of code is setting up the display for the Battleship game. Here's a breakdown of what
    # each part is doing:
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
    def draw_grid() -> None:
        """
        The function `draw_grid()` draws a grid on the screen using pygame with specified parameters.
        """
        for x in range(grid_x, grid_x + grid_width, cell_size):
            for y in range(grid_y, grid_y + grid_height, cell_size):
                rect = pygame.Rect(x, y, cell_size, cell_size)
                pygame.draw.rect(screen, BLACK, rect, 1)

    def draw_placed_ships() -> None:
        """
        The function `draw_placed_ships` iterates through each ship's coordinates and draws a rectangle
        representing the ship on the screen.
        """
        for ship in placed_ships:
            for (x, y) in ship[1]:
                rect = pygame.Rect(grid_x + x * cell_size, grid_y + y * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, LIGHT_BLUE, rect)

    def draw_labels() -> None:
        """
        The function `draw_labels` draws column labels (A-J) on the screen.
        """
        # Draw column labels (A-J)
        for col in range(cols):
            label = font.render(chr(ord('A') + col), True, BLACK)  # Convert col index to corresponding letter
            screen.blit(label, (grid_x + col * cell_size + (cell_size - label.get_width()) // 2, grid_y - label.get_height()))

       """
       The function `draw_labels` draws row labels (1-10) on the screen.
       """
        for row in range(rows):
            label = font.render(str(row + 1), True, BLACK)
            screen.blit(label, (grid_x - label.get_width(), grid_y + row * cell_size + (cell_size - label.get_height()) // 2))

    def valid_placement(ship_cells) -> bool:
        """
        The function `valid_placement` checks if a set of ship cells is within the bounds and does not
        overlap with any already placed ships.
        
        :param ship_cells: The `ship_cells` parameter is a list of tuples representing the cells that a
        ship will occupy on a game board. Each tuple contains the coordinates (x, y) of a cell where a
        part of the ship will be placed. The function `valid_placement` checks if the placement of the
        ship
        :return: a boolean value - True if the ship cells are valid for placement, and False if they are
        not valid (either out of bounds or overlapping another ship).
        """
        for (x, y) in ship_cells:
            if x < 0 or x >= cols or y < 0 or y >= rows:  # Out of bounds
                return False
            for placed_ship in placed_ships:
                if (x, y) in placed_ship[1]:  # Overlapping another ship
                    return False
        return True

    def preview_ship(mouse_pos, piece: Piece) -> List[tuple]:
        """
        The function `preview_ship` takes the mouse position and a game piece, calculates the preview
        cells for the piece placement, determines the color based on validity, and draws rectangles on
        the screen accordingly.
        
        :param mouse_pos: The `mouse_pos` parameter represents the current position of the mouse cursor
        on the screen. It is a tuple containing the x and y coordinates of the mouse cursor
        :param piece: Piece is a class representing a game piece or ship in a game. It likely contains
        information such as its shape, size, and possibly other attributes related to gameplay. In the
        provided code snippet, the function `preview_ship` takes the current mouse position and a `Piece`
        object as parameters to preview
        :type piece: Piece
        :return: The function `preview_ship` is returning a list of tuples representing the preview cells
        on the grid where the piece would be placed. Each tuple contains the x and y coordinates of a
        preview cell.
        """
        grid_x_pos = (mouse_pos[0] - grid_x) // cell_size
        grid_y_pos = (mouse_pos[1] - grid_y) // cell_size

        preview_cells = [(grid_x_pos + x, grid_y_pos + y) for y, row in enumerate(piece.shape) for x, cell in enumerate(row) if cell]

        color = GREEN if valid_placement(preview_cells) else RED

        for (x, y) in preview_cells:
            rect = pygame.Rect(grid_x + x * cell_size, grid_y + y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, color, rect)

        return preview_cells

    


    # `current_piece = player.takeSmallestPiece()` is assigning the smallest available piece from the
    # player's remaining unplaced pieces to the variable `current_piece`.
    current_piece = player.takeSmallestPiece() 
    while current_piece:
        # The code snippet `screen.fill(WHITE)`, `draw_grid()`, `draw_placed_ships()`, and
        # `draw_labels()` is responsible for setting up the initial display for the Battleship game
        # interface. Here's a breakdown of what each part is doing:
        screen.fill(WHITE)
        draw_grid()
        draw_placed_ships()
        draw_labels()  


     
       
      # This block of code is handling the interactive ship placement process in a Battleship game
      # using Pygame. Here's a breakdown of what each part is doing:
        mouse_pos = pygame.mouse.get_pos()

        current_ship_preview = preview_ship(mouse_pos, current_piece)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    current_piece = current_piece.rotated_right()  # Rotate the piece to the right

            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if valid_placement(current_ship_preview):
                    
                    # The code snippet `board.addPiece(current_piece, current_ship_preview[0][0],
                    # current_ship_preview[0][1])` is adding the current piece (ship) to the game
                    # board at the specified position. The `current_ship_preview[0][0]` and
                    # `current_ship_preview[0][1]` represent the x and y coordinates of the top-left
                    # cell where the ship will be placed on the grid.
                    board.addPiece(current_piece, current_ship_preview[0][0], current_ship_preview[0][1])
                    placed_ships.append((current_piece.columns(), current_ship_preview))

                   
                  # The code snippet you provided is responsible for printing the current state of the
                  # game board and the ships that have been placed by the player.
                    print("Current Board State:")
                    for row in board.grid:
                        print(['X' if tile.isHit() else ('P' if tile.getPiece() else '.') for tile in row])
                    print(f"{player.getName()} Placed Ships:", placed_ships)

                   
                   
                    current_piece = player.takeSmallestPiece()

                    print(f"Current Piece: {current_piece}")
                    print(f"Remaining Pieces: {player.unplacedPieces}")

                   
                    if current_piece is None:
                        print(f"{player.getName()} has placed all ships!")
                        break

        pygame.display.update()

    print(f"{player.getName()} has placed all ships!")
