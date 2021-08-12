import unittest
from src.murus_gallicus.piece import Piece
from src.murus_gallicus.constants import SPQR_RED, CELTIC_GREEN

class TestPiece(unittest.TestCase):
    """Class of Unit Tests to check bugs in the Piece Class."""

    def test_piece_well_initialized(self):
        """Test if a piece has the right when created."""
        piece = Piece(3,5,SPQR_RED)
        self.assertIsInstance(piece, Piece)
        self.assertEqual(piece.row, 3)
        self.assertEqual(piece.col, 5)
        self.assertEqual(piece.color, SPQR_RED)
        self.assertEqual(piece.stack_size, 2)

        piece = Piece(6,6,CELTIC_GREEN)
        self.assertIsInstance(piece, Piece)
        self.assertEqual(piece.row, 6)
        self.assertEqual(piece.col, 6)
        self.assertEqual(piece.color, CELTIC_GREEN)
        self.assertEqual(piece.stack_size, 2)

    def test_piece_direction(self):
        """Test if the piece can be well moved."""
        piece = Piece(3,4,CELTIC_GREEN)
        piece.move(5,6)
        self.assertEqual(piece.row, 5)
        self.assertEqual(piece.col, 6)

    def test_piece_becoming_wall_or_tower(self):
        """Test if a piece has the right stack size when become_wall() or become_tower() are called."""
        piece = Piece(0,2,CELTIC_GREEN)
        self.assertEqual(piece.stack_size, 2)
        piece.become_wall()
        self.assertIsInstance(piece, Piece)
        self.assertEqual(piece.stack_size, 1)
        piece.become_tower()
        self.assertIsInstance(piece, Piece)
        self.assertEqual(piece.stack_size, 2)

if __name__ == '__main__':
    unittest.main()
