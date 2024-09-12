import pygame
import sys
from testing_placement import ship_placement 

# Initialize Pygame
pygame.init()

# Set up display
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Battleship Game")

# Set background color to purple
background_colour = (236, 215, 240)  # Purple color

# Colors
black = (0, 0, 0)
light_blue = (173, 216, 230)

# Font
font = pygame.font.SysFont("Comic Sans MS", 30)
title_font = pygame.font.SysFont("Comic Sans MS", 50)  # Bigger font for title

# Button properties
button_rect = pygame.Rect(200, 250, 200, 80)  # Position (x, y) and size (width, height)

def draw_start_button():
    # Draw button background
    pygame.draw.rect(screen, light_blue, button_rect, border_radius=20)  # Rounded corners
    pygame.draw.rect(screen, black, button_rect, 3, border_radius=20)  # Border with rounded corners

    # Render button text
    text_surface = font.render("Start Game", True, black)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

def draw_title():
    # Render the title text
    title_surface = title_font.render("BATTLESHIP", True, black)
    title_rect = title_surface.get_rect(center=(width // 2, 100))  # Position at the top center
    screen.blit(title_surface, title_rect)

def main_menu():
    while True:
        screen.fill(background_colour)  # Fill background with purple

        draw_title()
        draw_start_button()  # Draw the start button

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Check for mouse click on button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    print("Start Game Clicked!")
                    # Call the ship placement screen
                    ship_placement()

        pygame.display.update()

if __name__ == "__main__":
    main_menu()

