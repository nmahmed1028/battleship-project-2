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

    # Check piece collision
    def test_piece_collision(self):
        board = Board()
        piece = Piece([
            [True, True], 
            [True, False]
        ])
        board.addPiece(piece, 1, 1)

        # These positions should have a piece on them
        piecePositions = [
            [1, 1],
            [1, 2],
            [2, 1]
        ]

        # Go through every position and make sure it either has a piece or not
        for y in range(0, 10):
            for x in range(0, 10):
                positionShouldHavePiece = False
                for position in piecePositions:
                    if [x, y] == position:
                        positionShouldHavePiece = True
                        break
                if positionShouldHavePiece:
                    self.assertIsNotNone(board.getPiece(x, y))
                else:
                    self.assertIsNone(board.getPiece(x, y))

    def test_has_end_game(self):
        board = Board()
        self.assertFalse(board.hasUnsunkShips())

        piece = Piece([
            [True, True], 
            [True, False]
        ])
        board.addPiece(piece, 1, 1)
        self.assertTrue(board.hasUnsunkShips())

        # Hit all the positions of the piece
        piecePositions = [
            [1, 1],
            [1, 2],
            [2, 1]
        ]

        for [x, y] in piecePositions:
            self.assertTrue(board.hit(x, y))
        
        self.assertFalse(board.hasUnsunkShips())

if __name__ == '__main__':
    unittest.main()