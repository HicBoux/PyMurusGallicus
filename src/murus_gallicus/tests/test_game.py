import unittest
from src.murus_gallicus.game import Game
from src.murus_gallicus.board import Board
from src.murus_gallicus.piece import Piece
from src.murus_gallicus.constants import SPQR_RED, CELTIC_GREEN, WINDOW

class TestGame(unittest.TestCase):
    """Class of Unit Tests to check bugs in the Game Class."""

    def test_game_creation(self):
        """Test if the attributes of a Game instance are well made when it's created."""
        game = Game(WINDOW, SPQR_RED)
        self.assertIsInstance(game, Game)
        self.assertEqual(game.selected, None)

        self.assertIsInstance(game.board, Board)
        self.assertEqual(len(game.board.board_grid), 7)
        self.assertIsInstance(game.board.board_grid[0][1], Piece)

        self.assertEqual(game.turn, SPQR_RED)
        self.assertEqual(game.window, WINDOW)
        self.assertEqual(game.is_over, False)
        self.assertEqual(game.winner, 0)

    def test_game_initialization(self):
        """Test if the attributes of a Game instance are well made when init(RGB_color) is called."""
        game = Game(WINDOW, CELTIC_GREEN)
        game.init(SPQR_RED)
        self.assertIsInstance(game, Game)
        self.assertEqual(game.selected, None)

        self.assertIsInstance(game.board, Board)
        self.assertEqual(len(game.board.board_grid), 7)
        self.assertIsInstance(game.board.board_grid[0][1], Piece)

        self.assertEqual(game.turn, SPQR_RED)
        self.assertEqual(game.window, WINDOW)
        self.assertEqual(game.is_over, False)
        self.assertEqual(game.winner, 0)

    def test_game_reset(self):
        """Test if the attributes of a Game instance are well made when reset(RGB_color) is called."""
        game = Game(WINDOW, CELTIC_GREEN)
        game.reset(SPQR_RED)
        self.assertIsInstance(game, Game)
        self.assertEqual(game.selected, None)

        self.assertIsInstance(game.board, Board)
        self.assertEqual(len(game.board.board_grid), 7)
        self.assertIsInstance(game.board.board_grid[0][1], Piece)

        self.assertEqual(game.turn, SPQR_RED)
        self.assertEqual(game.window, WINDOW)
        self.assertEqual(game.is_over, False)
        self.assertEqual(game.winner, 0)

    def test_game_over_check(self):
        """Test if the detection of a game over and of the winner is correctly done."""
        # Check if game over when the game is created
        game = Game(WINDOW, CELTIC_GREEN)
        self.assertEqual(game.check_if_over(), False)
        self.assertIsInstance(game.check_if_over(), bool)
        self.assertEqual(game.winner, 0)
        self.assertIsInstance(game.winner, int)
        # Check if game over when a piece of the player at top is put down on last row.
        new_board = Board(CELTIC_GREEN)
        new_board.board_grid[6][3] = Piece(6,3,SPQR_RED)
        game.board = new_board
        game.check_if_over()
        self.assertEqual(game.check_if_over(), True)
        self.assertIsInstance(game.check_if_over(), bool)
        self.assertEqual(game.winner, SPQR_RED)
        self.assertIsInstance(game.winner, tuple)
        # Check if game over when a player has only walls.
        game = Game(WINDOW, SPQR_RED)
        self.assertEqual(game.check_if_over(), False)
        self.assertIsInstance(game.check_if_over(), bool)
        all_pieces = game.board.get_all_same_color_pieces(SPQR_RED)
        for piece in all_pieces:
            piece.become_wall()
        self.assertEqual(game.check_if_over(), True)
        self.assertIsInstance(game.check_if_over(), bool)
        self.assertEqual(game.winner, CELTIC_GREEN)
        self.assertIsInstance(game.winner, tuple)

    def test_ai_move(self):
        """Test if the input board returned by the AI algorithm is well taken into account."""
        game = Game(WINDOW, CELTIC_GREEN)
        # Check piece color on top first row of the game board
        self.assertEqual(game.board.board_grid[0][0].color, SPQR_RED)
        # Check after a AI move where the color are reversed
        board = Board(SPQR_RED)
        game.ai_move(board)
        self.assertEqual(game.board.board_grid[0][0].color, CELTIC_GREEN)

if __name__ == '__main__':
    unittest.main()
