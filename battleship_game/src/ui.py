import pygame
import sys
from testing_placement import ship_placement 

# Initialize Pygame
pygame.init()

# Set up display
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Battleship Game")  # Corrected function name

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
    pygame.draw.rect(screen, light_blue, button_rect)  # No rounded corners
    pygame.draw.rect(screen, black, button_rect, 3)  # Border with no rounded corners

    text_surface = font.render("Start Game", True, black)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

def draw_title():
    title_surface = title_font.render("BATTLESHIP", True, black)
    title_rect = title_surface.get_rect(center=(width // 2, 100))  # Position at the top center
    screen.blit(title_surface, title_rect)

def start_game():
    while True:
        screen.fill(background_colour)  # Fill background with purple

        draw_title()
        draw_start_button()  # Draw the start button

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    print("Start Game Clicked!")
                    game_setup()
                    return

        pygame.display.update()

def game_setup():
    input_boxes = [
        # How many ships text box 
        pygame.Rect(380, 200, 140, 40), 
        # Player 1 Name text box
        pygame.Rect(380, 250, 140, 40), 
        # Player 2 Name text box 
        pygame.Rect(380, 300, 140, 40)   
    ]
    # Next button
    next_button_rect = pygame.Rect(250, 350, 100, 50)
    # Index of the active input box 
    active_box = None 
    # Text in the input boxes
    user_texts = ["", "", ""] 

    while True:
        # Fill background with purple
        screen.fill(background_colour)
          
        # Labels for input boxes
        labels = ["How many ships (1-5):", "Player 1 Name:", "Player 2 Name:"] 
         # Display labels 
        for i, label in enumerate(labels): 
            # Render text
            text_surface = font.render(label, True, black) 
            # Position text
            screen.blit(text_surface, (50, 200 + i * 50))

        # Display input boxes
        for i, box in enumerate(input_boxes): 
            pygame.draw.rect(screen, light_blue, box) 
            # Truncate text if it exceeds the box width
            truncated_text = user_texts[i]
            while font.size(truncated_text)[0] > box.width - 10:
                truncated_text = truncated_text[:-1]
            text_surface = font.render(truncated_text, True, black)
            screen.blit(text_surface, (box.x + 5, box.y + 5)) 

        pygame.draw.rect(screen, light_blue, next_button_rect)  
        next_text_surface = font.render("Next", True, black)
        # Center the text on the Next button
        next_text_rect = next_text_surface.get_rect(center=next_button_rect.center)
        # Display the text on the Next button
        screen.blit(next_text_surface, next_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the game
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_button_rect.collidepoint(event.pos):
                    try:
                        # Get the number of ships from the input
                        num_ships = int(user_texts[0])
                        # Validate the number of ships
                        if num_ships < 1 or num_ships > 5:
                            raise ValueError("Number of ships must be between 1 and 5.")
                        # Validate the player names
                        if not user_texts[1].isalpha() or not user_texts[2].isalpha():
                            raise ValueError("Player names must be strings and cannot contain numbers.")
                        print("Next Clicked!")
                        print("Ships:", num_ships)
                        print("Player 1:", user_texts[1])
                        print("Player 2:", user_texts[2])
                        # Proceed to the ship placement screen
                        ship_placement_screen(num_ships, user_texts[1], user_texts[2])
                        return
                    except ValueError as e:
                        # Print the error message
                        print(e)
                for i, box in enumerate(input_boxes):
                    if box.collidepoint(event.pos):
                        # Set the active input box
                        active_box = i
                        break

            if event.type == pygame.KEYDOWN and active_box is not None:
                if event.key == pygame.K_BACKSPACE:
                    # Remove the last character from the active input box
                    user_texts[active_box] = user_texts[active_box][:-1]
                else:
                    # Add the typed character to the active input box
                    user_texts[active_box] += event.unicode

        # Update the display
        pygame.display.update()

def ship_placement_screen(num_ships, name1, name2):
    print(f"Setting up game with {num_ships} ships for {name1} and {name2}")
    # add the logic to display the ship placement screen
    # For now, we'll just call the ship_placement function
    ship_placement()

if __name__ == "__main__":
    start_game()