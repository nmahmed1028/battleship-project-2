from typing import Self
from typing import List

# A battleship piece
class Piece:
    # Create a new piece with the given shape
    # The shape is represented as a grid of booleans, where True represents a filled cell
    # For example, a 3x3 L piece would be represented as:
    # [[True, False, False],
    #  [True, False, False],
    #  [True, True, True]]
    def __init__(self, shape: List[List[bool]]) -> None:
        self.shape = shape

    # Returns the number of rows in the piece
    def rows(self) -> int:
        return len(self.shape)
    
    # Returns the number of columns in the piece
    def columns(self) -> int:
        return len(self.shape[0])

    # Returns the piece rotated 90 degrees to the left
    def rotated_left(self) -> Self:
        rows = self.rows()
        cols = self.columns()
        # The new shape has the same dimensions as the old shape transposed
        shape = [[False for _ in range(rows)] for _ in range(cols)]
        
        for (y, row) in enumerate(self.shape):
            for (x, item) in enumerate(row):
                # Each item is moved to the transposed index with the rows flipped
                shape[cols - x - 1][y] = item
        return Piece(shape)

    # Returns the piece rotated 90 degrees to the right
    def rotated_right(self) -> Self:
        rows = self.rows()
        cols = self.columns()
        # The new shape has the same dimensions as the old shape transposed
        shape = [[False for _ in range(rows)] for _ in range(cols)]

        for (y, row) in enumerate(self.shape):
            for (x, item) in enumerate(row):
                # Each item is moved to the transposed index with the columns flipped
                shape[x][rows - y - 1] = item
        return Piece(shape)

    # Check if two pieces are equal
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.shape == other.shape
    
    # Return a string representation of the piece for debugging purposes
    def __repr__(self):
        return f"Piece({self.shape})"
