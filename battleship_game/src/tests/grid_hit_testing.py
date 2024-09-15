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

# Functions
def draw_grid():
    for x in range(0, width, cell_size):
        for y in range(0, height, cell_size):
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(screen, black, rect, 1)

def draw_ships():
    for ship in ships:
        for (x, y) in ship:
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, gray, rect)

def check_hit(x, y):
    for ship in ships:
        if (x, y) in ship:
            return True
    return False

def draw_guesses():
    for (x, y, hit) in guesses:
        color = red if hit else blue
        rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, color, rect)

# Main loop
while True:
    screen.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = mouse_x // cell_size
            grid_y = mouse_y // cell_size

            if (grid_x, grid_y) not in [(g[0], g[1]) for g in guesses]:
                hit = check_hit(grid_x, grid_y)
                guesses.append((grid_x, grid_y, hit))

    # Draw grid, ships (can be hidden), and guesses
    draw_grid()
    draw_ships()  # Comment out to hide ships
    draw_guesses()

    pygame.display.update()
