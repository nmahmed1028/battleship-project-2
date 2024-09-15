from .piece import Piece

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
    def getPiece(self) -> Piece | None:
        return self.piece
    
    # Mark the tile as hit 
    def markAsHit(self) -> None:
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
                    valid &= (self.getPiece(x + xOffset, y + yOffset) is None)
        return valid
    
    # Get the tile at a given location. If the location does not exist, return None
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
    
    # Hit a tile and return if there was a piece there
    def hit(self, x: int, y: int) -> bool:
        tile = self.getTile(x, y)
        if tile is None:
            return False

        tile.markAsHit()
        return not (tile.piece is None)
    
    # Check if there are any pieces left on the board
    def hasUnsunkShips(self) -> bool:
        for row in self.grid:
            for tile in row:
                if not (tile.piece is None) and not tile.isHit():
                    return True
        return False

    # Print the board for debugging purposes. Tiles are printed in a grid format with a character following this format:
    # |           | Hit | Not Hit |
    # | Has Piece |  X  |    O    |
    # | No Piece  |  .  |    -    |
    def print_board(self) -> None:
        for row in self.grid:
            row_str = ""
            for tile in row:
                if tile.isHit():
                    row_str += "X " if tile.piece else ". "
                else:
                    row_str += "O " if tile.piece else "- "
            print(row_str)

