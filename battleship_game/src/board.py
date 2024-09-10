# ETA: 1h
# Actual time: 52 min

import unittest
from piece import Piece

# A single tile on the battleship board
class Tile:
    def __init__(self) -> None:
        # The piece that is on this tile
        self.piece = None
        # If the tile has been hit yet
        self.hit = False

    # Add a piece to the tile. This should be called for every tile
    # that a piece is on when it is placed
    def addPiece(self, piece: Piece) -> None:
        self.piece = piece

    # Get the piece on this Tile or None if the tile is empty
    def piece(self) -> Piece | None:
        return self.piece
    
    # Mark the tile as hit 
    def hit(self) -> None:
        self.hit = True

    # Check if the tile has been hit yet
    def isHit(self) -> bool:
        return self.hit

# A board that stores each piece that has been placed at it's location
class Board:
    def __init__(self) -> None:
        self.grid = [[Tile() for _ in range(10)] for _ in range(10)]

    # Add a piece to the board an offset
    def addPiece(self, piece: Piece, x: int, y: int) -> None:
        for [yOffset, row] in enumerate(piece.shape):
            for [xOffset, item] in enumerate(row):
                if item:
                    self.getTile(x+xOffset, y+yOffset).addPiece(piece)

    # Check if placing a piece at a location would collide with other pieces
    def piecePlacementValid(self, piece: Piece, x: int, y: int) -> bool:
        valid = True
        for [yOffset, row] in enumerate(piece.shape):
            for [xOffset, item] in enumerate(row):
                if item:
                    valid &= not (self.getPiece(x + xOffset, y + yOffset) is None)
        return valid
    
    def getTile(self, x: int, y: int) -> Tile | None:
        if len(self.grid) <= y:
            return None
        row = self.grid[y]
        if len(row) <= x:
            return None
        return row[x]
    
    # Get the piece at a given location
    def getPiece(self, x: int, y: int) -> Piece | None:
        tile = self.getTile(x, y)
        if tile is None:
            return None
        return tile.piece
