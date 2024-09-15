# ui.py
import pygame
import sys
from .player import Player
from .config import BACKGROUND_COLOR, BLACK, LIGHT_BLUE, FONT_NAME, FONT_SIZE, TITLE_FONT_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH


# Initialize fonts
pygame.font.init()
font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
title_font = pygame.font.SysFont(FONT_NAME, TITLE_FONT_SIZE)

# Button properties
button_rect = pygame.Rect(200, 250, 200, 80)  # Position (x, y) and size (width, height)


def draw_button(screen, text, rect, font):
    pygame.draw.rect(screen, LIGHT_BLUE, rect)
    pygame.draw.rect(screen, BLACK, rect, 3)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def draw_title(screen, text, font):
    title_surface = font.render(text, True, BLACK)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(title_surface, title_rect)

def start_game(screen):
    while True:
        screen.fill(BACKGROUND_COLOR)
        
        draw_title(screen, "BATTLESHIP", title_font)
        button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
        draw_button(screen, "Start Game", button_rect, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    print("Start Game Clicked!")
                    return

        pygame.display.update()

def game_setup(screen):
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
        screen.fill(BACKGROUND_COLOR)
          
        # Labels for input boxes
        labels = ["How many ships (1-5):", "Player 1 Name:", "Player 2 Name:"] 
         # Display labels 
        for i, label in enumerate(labels): 
            # Render text
            text_surface = font.render(label, True, BLACK) 
            # Position text
            screen.blit(text_surface, (50, 200 + i * 50))

        # Display input boxes
        for i, box in enumerate(input_boxes): 
            pygame.draw.rect(screen, LIGHT_BLUE, box) 
            # Truncate text if it exceeds the box width
            truncated_text = user_texts[i]
            while font.size(truncated_text)[0] > box.width - 10:
                truncated_text = truncated_text[:-1]
            text_surface = font.render(truncated_text, True, BLACK)
            screen.blit(text_surface, (box.x + 5, box.y + 5)) 

        pygame.draw.rect(screen, LIGHT_BLUE, next_button_rect)  
        next_text_surface = font.render("Next", True, BLACK)
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
                        return num_ships, user_texts[1], user_texts[2]
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

def switch_player_screen(screen):
    next_button_rect = pygame.Rect(0, 0, 100, 50)
    next_button_rect.bottomright = (SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20)

    while True:
        screen.fill(BACKGROUND_COLOR)
        
        draw_title(screen, "Switch players", title_font)
        draw_button(screen, "Next", next_button_rect, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_button_rect.collidepoint(event.pos):
                    print("Next Clicked!")
                    return

        pygame.display.update()


def end_game(screen, winner: Player):
    while True:
        # Fill background with purple
        screen.fill(BACKGROUND_COLOR)
        
        # Render "Game Over" text
        game_over_surface = title_font.render("Game Over", True, BLACK)
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(game_over_surface, game_over_rect)
        
        # Render "Player X Won" text
        winner_surface = font.render(f"{winner} Won!", True, BLACK)
        winner_rect = winner_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(winner_surface, winner_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the game
                pygame.quit()
                sys.exit()

        # Update the display
        pygame.display.update()
        
if __name__ == "__main__":
    start_game()