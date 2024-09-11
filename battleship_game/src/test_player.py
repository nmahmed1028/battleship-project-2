import unittest
from piece import Piece
from player import Player

# Tests for the board
class TestPlayerMethods(unittest.TestCase):
    def test_take_smallest_piece(self):
        player = Player()
        for x in range(1, 6):
            piece = player.takeSmallestPiece()
            self.assertEqual(piece.shape, [[True for _ in range(x)]])

if __name__ == '__main__':
    unittest.main()