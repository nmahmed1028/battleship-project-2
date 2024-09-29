# ui.py
import pygame
import sys
from .board_mechanics.player import Player
from .config import BACKGROUND_COLOR, BLACK, LIGHT_BLUE, FONT_NAME, FONT_SIZE, TITLE_FONT_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH


# Initialize fonts
pygame.font.init()
font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
title_font = pygame.font.SysFont(FONT_NAME, TITLE_FONT_SIZE)

# Button properties
button_rect = pygame.Rect(200, 250, 200, 80)  # Position (x, y) and size (width, height)


def draw_button(screen, text, rect, font):
    """
    Draws a button with text on the given screen.

    Args:
        screen (pygame.Surface): The surface on which to draw the button.
        text (str): The text to display on the button.
        rect (pygame.Rect): The rectangle defining the button's position and size.
        font (pygame.font.Font): The font used to render the text.

    Returns:
        None
    """
    # Draw the button background
    pygame.draw.rect(screen, LIGHT_BLUE, rect)
    # Draw the button border
    pygame.draw.rect(screen, BLACK, rect, 3)
    # Render the button text
    text_surface = font.render(text, True, BLACK)
    # Center the text on the button
    text_rect = text_surface.get_rect(center=rect.center)
    # Display the text on the button
    screen.blit(text_surface, text_rect)

def draw_title(screen, text, font):
    # Render the title text
    title_surface = font.render(text, True, BLACK)
    # Center the title text on the screen
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    # Display the title text
    screen.blit(title_surface, title_rect)

def start_game(screen):
    """
    The function `start_game` creates a game screen with a title and a start button that exits the game
    when clicked.
    
    :param screen: The `screen` parameter in the `start_game` function is typically a reference to the
    display surface where all the graphical elements of the game will be drawn. This surface is created
    using a library like Pygame and represents the visible area of the game window where you can render
    graphics, text, and
    :return: The `start_game` function returns when the "Start Game" button is clicked.
    """
    while True:
        # Fill background with the specified color
        screen.fill(BACKGROUND_COLOR)
        
        # Draw the title
        draw_title(screen, "BATTLESHIP", title_font)
        # Center the button on the screen
        button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
        # Draw the start button
        draw_button(screen, "Start Game", button_rect, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the game
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    # Print a message and return when the button is clicked
                    print("Start Game Clicked!")
                    return

        # Update the display
        pygame.display.update()

def game_setup(screen):
    """
    The `game_setup` function sets up a game screen with input boxes for number of ships and player
    names, allowing users to input data and proceed to the next step.
    
    :param screen: The `screen` parameter in the `game_setup` function represents the surface where all
    the game elements will be drawn. It is typically the main surface where the game graphics are
    displayed, and it is provided by the Pygame library
    :return: The `game_setup` function returns a tuple containing the number of ships, Player 1's name,
    and Player 2's name. The values are extracted from the input boxes filled by the user before
    clicking the "Next" button.
    """
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
            # Draw the input box
            pygame.draw.rect(screen, LIGHT_BLUE, box) 
            # Truncate text if it exceeds the box width
            truncated_text = user_texts[i]
            while font.size(truncated_text)[0] > box.width - 10:
                truncated_text = truncated_text[:-1]
            # Render the truncated text
            text_surface = font.render(truncated_text, True, BLACK)
            # Display the text inside the input box with some padding
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


def single_player_setup(screen):
    """
    Set up a single player game where the player plays against an AI.
    Similar to game_setup() function
    
    :param screen: The pygame screen to display the setup UI.
    :return: Tuple containing number of ships, human player name, and AI difficulty level.
    """

    input_boxes = [
        pygame.Rect(380, 200, 140, 40), #how many ships text box
        pygame.Rect(380, 250, 140, 40), #player name text box
        pygame.Rect(580, 300, 140, 40) #ai difficulty text box
    ]

    next_button_rect = pygame.Rect(250, 350, 100, 50)
    active_box = None
    user_texts = ["", "", ""] #text for num ships, player name, ai difficulty

    while True:
        screen.fill(BACKGROUND_COLOR)
        labels = ["How many ships (1-5):", "Player Name:", "AI Difficulty (easy, medium, hard)"]
        for i, label in enumerate(labels):
            text_surface = font.render(label, True, BLACK)
            screen.blit(text_surface, (50, 200 + i * 50))
        
        for i, box in enumerate(input_boxes):
            pygame.draw.rect(screen, LIGHT_BLUE, box)
            truncated_text = user_texts[i]
            while font.size(truncated_text)[0] > box.width - 10:
                truncated_text = truncated_text[:-1]
            text_surface = font.render(truncated_text, True, BLACK)
            screen.blit(text_surface, (box.x + 5, box.y + 5))
        
        pygame.draw.rect(screen, LIGHT_BLUE, next_button_rect)
        next_text_surface = font.render("Next", True, BLACK)
        next_text_rect = next_text_surface.get_rect(center = next_button_rect.center)
        screen.blit(next_text_surface, next_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_button_rect.collidepoint(event.pos):
                    try:
                        num_ships = int(user_texts[0])
                        if num_ships < 1 or num_ships > 5:
                            raise ValueError("Number of ships must be between 1 and 5.")
                        if not user_texts[1].isalpha():
                            raise ValueError("Player name must be a string.")
                        if user_texts[2].lower() not in ["easy", "medium", "hard"]:
                            raise ValueError("AI difficulty must be 'easy', 'medium', or 'hard'.")
                        print("Next Clicked!")
                        return num_ships, user_texts[1], user_texts[2].lower()
                    except ValueError as err:
                        print(err)
                
                for i, box in enumerate(input_boxes):
                    if box.collidepoint(event.pos):
                        active_box = i
                        break
            
            if event.type == pygame.KEYDOWN and active_box is not None:
                if event.key == pygame.K_BACKSPACE:
                    user_texts[active_box] = user_texts[active_box][:-1]
                else:
                    user_texts[active_box] += event.unicode
        pygame.display.update()

def switch_player_screen(screen):
    """
    The function `switch_player_screen` creates a screen with a "Next" button and waits for the button
    to be clicked before returning.
    
    :param screen: The `screen` parameter in the `switch_player_screen` function is typically a
    reference to the surface where you draw all the elements of your game or application using the
    Pygame library. This surface represents the visible window or screen where graphics are displayed
    :return: The `switch_player_screen` function returns when the "Next" button is clicked.
    """
    print("Switching players screen")
    # Define the "Next" button rectangle
    next_button_rect = pygame.Rect(0, 0, 100, 50)
    # Position the "Next" button at the bottom right corner with some padding
    next_button_rect.bottomright = (SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20)

    while True:
        # Fill background with the specified color
        screen.fill(BACKGROUND_COLOR)
        
        # Draw the title
        draw_title(screen, "Switch players", title_font)
        # Draw the "Next" button
        draw_button(screen, "Next", next_button_rect, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the game
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_button_rect.collidepoint(event.pos):
                    # Print a message and return when the button is clicked
                    print("Next Clicked!")
                    return

        # Update the display
        pygame.display.update()


def end_game(screen, winner: Player):
    """
    The `end_game` function displays a "Game Over" message and the winning player's name on the screen
    until the user closes the window.
    
    :param screen: The `screen` parameter in the `end_game` function is typically a reference to the
    surface where all the graphical elements of the game are drawn. It is usually created using the
    `pygame.display.set_mode()` function and represents the game window or display area. This surface is
    where you render all the
    :param winner: The `winner` parameter in the `end_game` function represents the player who has won
    the game. It is of type `Player`, which likely refers to a class or object representing a player in
    the game. The function uses this parameter to display a message indicating which player has won the
    game
    :type winner: Player
    """
    while True:
        # Fill background with the specified color
        screen.fill(BACKGROUND_COLOR)
        
        # Render "Game Over" text
        game_over_surface = title_font.render("Game Over", True, BLACK)
        # Center the "Game Over" text on the screen
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        # Display the "Game Over" text
        screen.blit(game_over_surface, game_over_rect)
        
        # Render "Player X Won" text
        winner_surface = font.render(f"{winner} Won!", True, BLACK)
        # Center the "Player X Won" text on the screen
        winner_rect = winner_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        # Display the "Player X Won" text
        screen.blit(winner_surface, winner_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the game
                pygame.quit()
                sys.exit()

        # Update the display
        pygame.display.update()


def select_game_mode(screen): #choose if you want to play against an ai or another player
    """
    Displays a screen for selecting either single-player or multiplayer mode.
    
    :param screen: The game screen where the game mode selection is displayed.
    :return: Returns 'single' if the player selects single-player mode, otherwise 'multi'.
    """
    sp_button_rect = pygame.Rect(0, 0, 200, 80) #rectangle for single player button
    mp_button_rect = pygame.Rect(0, 0, 200, 80) #rectangle for multi player button

    #position the two buttons
    sp_button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
    mp_button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)

    while True:
        screen.fill(BACKGROUND_COLOR) #fill background
        draw_title(screen, "Select Game Mode", title_font) #draw title

        #draw buttons
        draw_button(screen, "Single Player", sp_button_rect, font)
        draw_button(screen, "Multiplayer", mp_button_rect, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if player x's out of window at any point, exit the game
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN: #if player clicks down
                if sp_button_rect.collidepoint(event.pos): #if player clicks on single player, return single
                    print("Single Player selected")
                    return "single"
                elif mp_button_rect.collidepoint(event.pos): #if player clicks on multi player, return multi
                    print("Multiplayer selected")
                    return "multi"
        
        pygame.display.update()


def select_ai_difficulty(screen):
    """
    Displays a screen for selecting AI difficulty level (easy, medium, hard).
    
    :param screen: The game screen where the AI difficulty selection is displayed.
    :return: Returns 'easy', 'medium', or 'hard' based on player's choice.
    """
    ebutton_rect = pygame.Rect(0, 0, 200, 80) #rectangle for easy difficulty button
    mbutton_rect = pygame.Rect(0, 0, 200, 80) #rectangle for medium difficulty button
    hbutton_rect = pygame.Rect(0, 0, 200, 80) #rectangle for hard difficulty button

    #positions buttons
    ebutton_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
    mbutton_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    hbutton_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)

    while True:
        screen.fill(BACKGROUND_COLOR) #fill background 
        draw_title(screen, "Select AI Difficulty", title_font) #display title

        #draw the three buttons
        draw_button(screen, "Easy", ebutton_rect, font)
        draw_button(screen, "Medium", mbutton_rect, font)
        draw_button(screen, "Hard", hbutton_rect, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if player x's out of window at any point, exit the game
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ebutton_rect.collidepoint(event.pos):
                    print("Easy AI selected")
                    return "easy"
                elif mbutton_rect.collidepoint(event.pos):
                    print("Medium AI selected")
                    return "medium"
                elif hbutton_rect.collidepoint(event.pos):
                    print("Hard AI selected")
                    return "hard"
            
        pygame.display.update()


        
if __name__ == "__main__":
    start_game()