import unittest
from ..board_mechanics import piece

# A battleship piece
# This Python unittest class tests the rotation methods of a custom Piece class.
class TestPieceMethods(unittest.TestCase):
    def test_rotate_left(self):
        """
        The function `test_rotate_left` tests the `rotated_left` method of a `Piece` class by comparing
        the rotated piece with an expected rotated piece.
        """
        self.assertEqual(
            piece.Piece([
                [True, False], 
                [False, False]
            ]).rotated_left(),
            piece.Piece([
                [False, False], 
                [True, False]
            ])
        )
    
    def test_rotate_left_long(self):
        """
        The function `test_rotate_left_long` tests the `rotated_left` method of a `Piece` class by
        comparing the rotated piece with a specific arrangement of boolean values.
        """
        self.assertEqual(
            piece.Piece([
                [True, False]
            ]).rotated_left(),
            piece.Piece([
                [False], 
                [True]
            ])
        )

    def test_rotate_right(self):
        """
        The function `test_rotate_right` tests the `rotated_right` method of a `Piece` class by
        comparing the rotated piece with an expected piece configuration.
        """
        self.assertEqual(
            piece.Piece([
                [True, False], 
                [False, False]
            ]).rotated_right(),
            piece.Piece([
                [False, True], 
                [False, False]
            ])
        )

    def test_rotate_right_long(self):
        """
        The function `test_rotate_right_long` tests the `rotated_right` method of a `Piece` class by
        comparing the rotated piece with a specific arrangement of boolean values.
        """
        self.assertEqual(
            piece.Piece([
                [True, False]
            ]).rotated_right(),
            piece.Piece([
                [True], 
                [False]
            ])
        )

if __name__ == '__main__':
    unittest.main()