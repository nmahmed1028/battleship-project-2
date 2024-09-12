import unittest
import piece

# A battleship piece
class TestPieceMethods(unittest.TestCase):
    def test_rotate_left(self):
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
        self.assertEqual(
            piece.Piece([
                [True, False]
            ]).rotated_left(),
            piece.Piece([
                [True], 
                [False]
            ])
        )

    def test_rotate_right(self):
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
        self.assertEqual(
            piece.Piece([
                [True, False]
            ]).rotated_left(),
            piece.Piece([
                [False], 
                [True]
            ])
        )

if __name__ == '__main__':
    unittest.main()