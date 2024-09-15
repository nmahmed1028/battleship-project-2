# Architecture

This battleship project is implemented with python and pygame. 

The entry point for the program is [run_game.py](run_game.py). It defines the core loop for rendering and player interaction

TODO: _ defines the UI for the screen transitions
TODO: _ defines the UI for board setup
TODO: _ defines the UI for hitting ships

Important classes:
- [Player](../battleship_game/src/player.py): The player state includes the battleship pieces they have not placed yet and the state of their board
- [Board](../battleship_game/src/board.py): Defines the board with a grid of tiles. The board is used to keep track of where ships are placed and what tiles have been hit. The board also knows how to hit and place ships
    - [Tile](../battleship_game/src/board.py): Each tile in the board has information about if it has been hit and what piece has been placed on top of it
- [Piece](../battleship_game/src/piece.py): Each piece is a ship that may be placed on a board. Pieces can also be rotated left and right
