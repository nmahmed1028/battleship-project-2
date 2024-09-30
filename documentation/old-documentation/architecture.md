# Architecture

This battleship project is implemented with python and pygame. 

# Game Flow

The entry point for the program is [run_game.py](../run_game.py); To understand how the Battleship game scripts are connected and executed, follow the flow from running the game to the end of the game cycle:

1. **`run_game.py`**: Entry point for launching the game.
2. **`main.py`**: Initializes Pygame and creates an instance of the `Game` class.
3. **`game.py`**: Contains the `Game` class which manages the game state and flow.
4. **`ui.py`**: Provides functions for rendering different game screens (e.g., start screen, game setup, etc.).
5. **`board_mechanics/player.py`**: Defines the `Player` class and manages player-specific operations.
6. **`board_mechanics/board.py`**: Manages the game board and its state.
7. **`board_mechanics/piece.py`**: Defines the `Piece` class and handles ship pieces and their operations.
8. **`game_mechanics/place_ships.py`**: Handles the ship placement logic and rendering on the game board.
9. **`game_mechanics/attack.py`**: Manages the attack logic and determines the winner.

This list illustrates the sequence of script execution from starting the game to handling gameplay mechanics.


# Detailed Game flow:
- [run_game.py](../run_game.py): A lightweight script to launch the Battleship game by calling the `main()` function from the `main.py` module.
    - **Purpose**: Provides a clean entry point to run the Battleship game without directly invoking the `main.py` module, helping to keep the structure of the project modular and clean.
    - **Functionality**:
        - **`if __name__ == "__main__":`**: When this script is executed, it imports the `main()` function from the `battleship_game.src.main` module and calls it to start the game.
    - **Usage**:
        - Run this script to start the Battleship game by executing the following command:
        ```bash
        python run_game.py
        ```

- [main.py](../battleship_game/src/main.py): The entry point for initializing and running the Battleship game using Pygame.
    - **Functions**:
        - **`main()`**: Initializes the Pygame library, sets up the game display, creates an instance of the `Game` class, and starts the game loop.
            - **Pygame Initialization**: Calls `pygame.init()` to initialize Pygame modules.
            - **Display Setup**: Sets up the game screen with the defined width and height from `config.py`, and sets the game window caption.
            - **Game Instance Creation**: Initializes the `Game` class with the Pygame screen object, setting up the state and mechanics for the Battleship game.
            - **Game Execution**: Calls the `run()` method of the `Game` instance to start the game logic, including displaying the start screen and handling game flow.
    - **Usage**:
        - This module can be run directly to launch the Battleship game.
        - It includes a relative import of `tests` to ensure proper functioning during test execution.
    - **Execution**:
        - If executed as the main program (`__main__`), the `main()` function is called, starting the Battleship game.

- [game.py](../battleship_game/src/game.py): Orchestrates the overall game flow, including game setup, ship placement, attack simulation, and game state transitions.
    - **`Game`**: This class manages the different stages of the Battleship game, from setup to the endgame.
        - **`__init__`**: Initializes the game object with the screen, game state, number of ships, and player information.
        - **`run`**: Runs the main game loop, transitioning between different game states (start screen, setup, ship placement, and main game). It manages the setup of players, placement of ships, and handles the attack phase until the game ends.


- [ui.py](../battleship_game/src/ui.py): Handles the user interface for the game, managing screen transitions, button rendering, and user input.
    - **`start_game`**: Displays the title screen with a "Start Game" button. When clicked, the game begins.
    - **`game_setup`**: Manages the setup screen where players input the number of ships and their names. Validates inputs before transitioning to the ship placement screen.
    - **`switch_player_screen`**: Displays a screen that prompts players to switch turns with a "Next" button to continue the game.
    - **`end_game`**: Shows the game over screen, displaying which player won and ending the game.
    - **`draw_button`**: A helper function to draw clickable buttons on the screen.
    - **`draw_title`**: A helper function to render centered titles on the screen.


- [Player](../battleship_game/src/board_mechanics/player.py): The player state includes the battleship pieces they have not placed yet and the state of their board
- [Board](../battleship_game/src/board_mechanics/board.py): Defines the board with a grid of tiles. The board is used to keep track of where ships are placed and what tiles have been hit. The board also knows how to hit and place ships
    - [Tile](../battleship_game/src/board_mechanics/board.py): Each tile in the board has information about if it has been hit and what piece has been placed on top of it
- [Piece](../battleship_game/src/board_mechanics/piece.py): Each piece is a ship that may be placed on a board. Pieces can also be rotated left and right


- [place_ships.py](../battleship_game/src/game_mechanics/place_ships.py): Manages the ship placement process for each player, handling ship previews, validations, and placement on the game board.
    - **Functions**:
        - **`ship_placement(screen, player)`**: The main function that facilitates the ship placement process for a given player. It handles grid rendering, ship placement, and validation.
        - **`draw_grid()`**: Draws a 10x10 grid on the screen to represent the battleship board.
        - **`draw_placed_ships()`**: Draws ships that have already been placed by the player on the grid.
        - **`draw_labels()`**: Draws labels for rows (1-10) and columns (A-J) around the grid for easy referencing.
        - **`valid_placement(ship_cells)`**: Validates if a ship's placement is within the grid boundaries and does not overlap with already placed ships.
        - **`preview_ship(mouse_pos, piece)`**: Displays a preview of the current ship at the mouse position, changing the color to green if valid and red if invalid.
    - **Main loop**:
        - The function enters a loop where the player places each ship on the grid.
        - The current ship is highlighted at the mouse position.
        - The player can rotate the ship using the 'R' key.
        - When a valid position is clicked, the ship is placed on the backend board, and the next ship is selected until all ships are placed.
    - **Backend interaction**:
        - Ships are placed on a backend `Board` object, updating the grid representation and ensuring correct gameplay mechanics.
        - The function interacts with the `Piece` class to retrieve ship shapes and handle ship rotation.
    - **Ship validation and placement**:
        - Validates ship placement by checking boundaries and overlaps.
        - Once the ship is validly placed, it updates the board and stores the ship's position.
    - **Dynamic display updates**:
        - The screen is updated after every ship preview or placement, providing real-time feedback to the player.
        - The function also dynamically updates the game's window title to show which player is placing ships.

- [attack.py](../battleship_game/src/game_mechanics/attack.py): Manages the main attack phase of the game, including the handling of attacks, grid drawing, and the determination of hits and misses.
    - **`Attack`**: This class is responsible for handling the gameplay mechanics when players attack each other's boards. It includes methods for drawing grids, handling attacks, displaying scores, and simulating the attack process.
        - **`__init__`**: Initializes the attack system, including players, screen, fonts, and scores.
        - **`draw_grid`**: Draws the player's or opponent's board with ship positions hidden or visible based on the game state.
        - **`handle_attack`**: Handles the logic when a player clicks to attack a tile on the opponent's board, marking it as hit or missed.
        - **`draw_text`**: A helper function to render text on the screen.
        - **`draw_scores`**: Displays the current scores for both players on the screen.
        - **`attack`**: The main loop that handles a player's attack turn. It checks for hits and updates the board accordingly.
        - **`show_popup`**: Displays a temporary popup message (e.g., for hit or miss) during gameplay.
        - **`attack_simulation`**: Simulates the entire attack phase, alternating turns between players until one wins.