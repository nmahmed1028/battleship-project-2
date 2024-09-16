# The TestPlayerMethods class contains unit tests for the Player class methods in a board game
# implementation.
import unittest
from ..board_mechanics.piece import Piece
from ..board_mechanics.player import Player

# Tests for the board
class TestPlayerMethods(unittest.TestCase):
    def test_take_smallest_piece(self):
        """
        The function `test_take_smallest_piece` tests the `takeSmallestPiece` method of the `Player`
        class by asserting the shape of the piece taken by the player.
        """
        player = Player("Player 1", 5)
        for x in range(1, 6):
            piece = player.takeSmallestPiece()
            self.assertEqual(piece.shape, [[True for _ in range(x)]])

    def test_player_construction(self):
        """
        The function `test_player_construction` creates a player object with a specified name and number
        of unplaced pieces.
        """
        player = Player("Player 1", 3)
        player.unplacedPieces = [
            Piece([[True, True, True]]),
            Piece([[True, True]]),
            Piece([[True]])
        ]

if __name__ == '__main__':
    unittest.main()