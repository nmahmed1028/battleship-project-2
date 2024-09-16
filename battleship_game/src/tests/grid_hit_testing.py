import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 600, 600
rows, cols = 10, 10  # Battleship grid is 10x10
cell_size = width // cols
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Battleship Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
gray = (200, 200, 200)

# Ships (hard-coded for simplicity)
ships = [
    [(1, 1), (1, 2), (1, 3)],  # Ship 1 (3 cells)
    [(3, 4), (4, 4), (5, 4)],  # Ship 2 (3 cells)
    [(6, 6), (6, 7)],          # Ship 3 (2 cells)
]

# Player guesses
guesses = []


def draw_grid():
    """
    The function `draw_grid` creates a grid of rectangles on the screen using pygame.
    """
    for x in range(0, width, cell_size):
        for y in range(0, height, cell_size):
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(screen, black, rect, 1)

def draw_ships():
    """
    The function `draw_ships` iterates through a list of ships and draws rectangles representing each
    ship on the screen using Pygame.
    """
    for ship in ships:
        for (x, y) in ship:
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, gray, rect)

def check_hit(x, y):
    """
    The function `check_hit` checks if a given coordinate (x, y) is a hit on any of the ships on the
    board.
    """
    for ship in ships:
        if (x, y) in ship:
            return True
    return False

def draw_guesses():
    """
    The function `draw_guesses` iterates through a list of guesses and draws rectangles on the screen
    based on the coordinates and hit status of each guess.
    """
    for (x, y, hit) in guesses:
        color = red if hit else blue
        rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, color, rect)


# Main game loop: This loop continues running until the user closes the game
while True:
    # Fill the screen with a white background to clear it before each frame
    screen.fill(white)

    # Handle events (input from the user, such as mouse clicks and window close events)
    for event in pygame.event.get():
        # Check if the user has clicked the close button (exit the game)
        if event.type == pygame.QUIT:
            pygame.quit()  # Quit the game
            sys.exit()     # Exit the Python script

        # Check if the user has clicked the mouse button
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position in pixels
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Convert pixel coordinates to grid coordinates (based on the size of each cell)
            grid_x = mouse_x // cell_size
            grid_y = mouse_y // cell_size

            # If the player hasn't already guessed this spot
            if (grid_x, grid_y) not in [(g[0], g[1]) for g in guesses]:
                # Check if the guess is a hit on a ship
                hit = check_hit(grid_x, grid_y)
                # Add the guess (grid_x, grid_y) and whether it was a hit (True or False) to the list of guesses
                guesses.append((grid_x, grid_y, hit))

    # Draw the grid of the game
    draw_grid()
    
    # Draw the ships on the grid (if needed, you can comment this line out to hide the ships)
    draw_ships()  # Comment out to hide ships
    
    # Draw the player's guesses (red for hits, blue for misses)
    draw_guesses()

    # Update the display to show the newly drawn frame
    pygame.display.update()
