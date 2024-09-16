# config.py
"""
Configuration settings for the Battleship game.

This module contains constants used throughout the game, including screen dimensions,
colors, font settings, board settings, and button properties.

Attributes:
    SCREEN_WIDTH (int): The width of the game screen.
    SCREEN_HEIGHT (int): The height of the game screen.
    WHITE (tuple): RGB color code for white.
    BLACK (tuple): RGB color code for black.
    RED (tuple): RGB color code for red.
    GREEN (tuple): RGB color code for green.
    BLUE (tuple): RGB color code for blue.
    GRAY (tuple): RGB color code for gray.
    LIGHT_BLUE (tuple): RGB color code for light blue.
    DARK_GRAY (tuple): RGB color code for dark gray.
    BACKGROUND_COLOR (tuple): RGB color code for the background color.
    FONT_NAME (str): The name of the font used in the game.
    FONT_SIZE (int): The size of the font used for general text.
    TITLE_FONT_SIZE (int): The size of the font used for titles.
    ROWS (int): The number of rows in the game board.
    COLS (int): The number of columns in the game board.
    CELL_SIZE (int): The size of each cell in the game board.
    PLAYER_BOARD_OFFSET_X (int): The x-offset for the player's board.
    OPPONENT_BOARD_OFFSET_X (int): The x-offset for the opponent's board.
    BOARD_OFFSET_Y (int): The y-offset for both boards.
    BUTTON_RECT (pygame.Rect): The rectangle defining the position and size of a button.
"""
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