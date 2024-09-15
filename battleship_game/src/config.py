# config.py
import pygame

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors (RGB format)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
DARK_GRAY = (50, 50, 50)

# Background color
BACKGROUND_COLOR = (236, 215, 240)  # Purple color

# Font settings
FONT_NAME = "Comic Sans MS"
FONT_SIZE = 30
TITLE_FONT_SIZE = 50

# Board settings
ROWS = 10
COLS = 10
CELL_SIZE = 30

# Board offsets
PLAYER_BOARD_OFFSET_X = 400  # Right side
OPPONENT_BOARD_OFFSET_X = 50  # Left side
BOARD_OFFSET_Y = 100

# Button properties
BUTTON_RECT = pygame.Rect(350, 500, 100, 50)  # Position (x, y) and size (width, height)