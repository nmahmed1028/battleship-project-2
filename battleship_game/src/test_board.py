import unittest
import piece
from board import Board, Tile
from piece import Piece

# Tests for the board
class TestBoardMethods(unittest.TestCase):
    def test_place_piece(self):
        board = Board()
        piece = Piece([
            [True, False], 
            [True, False]
        ])
        for y in range(0, 10, 2):
            for x in range(0, 10):
                board.addPiece(piece, x, y)
    
    def test_piece_placement_valid(self):
        board = Board()
        piece = Piece([
            [True]
        ])
        board.addPiece(piece, 0, 0)
        self.assertFalse(board.piecePlacementValid(piece, 0, 0))

if __name__ == '__main__':
    unittest.main()