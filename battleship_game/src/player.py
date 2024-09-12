import unittest
from piece import Piece
from typing import List
from board import Board

# The pieces each player starts with in the game
STARTING_PIECES: List[Piece] = [
    Piece([[True, True, True, True, True]]),
    Piece([[True, True, True, True]]),
    Piece([[True, True, True]]),
    Piece([[True, True]]),
    Piece([[True]]),
]

# A player in the battleship game
class Player:
    def __init__(self, name: str, numberOfShips: int) -> None:
        self.name = name
        self.unplacedPieces = STARTING_PIECES[len(STARTING_PIECES) - numberOfShips:]
        self.board = Board()

    # Take the smallest piece (out of 5 long pieces) and return it
    # or None if all pieces have been taken
    def takeSmallestPiece(self) -> Piece | None:
        return self.unplacedPieces.pop()
    
    # Get the player's name
    def getName(self) -> str:
        return self.name
