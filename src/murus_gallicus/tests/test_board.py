import unittest
from src.murus_gallicus.board import Board
from src.murus_gallicus.piece import Piece
from src.murus_gallicus.constants import SPQR_RED, CELTIC_GREEN

class TestBoard(unittest.TestCase):
    """Class of Unit Tests to check bugs in the Board Class."""

    def test_board_grid_is_7_x_8(self):
        """Test if the board grid is composed by 7x8 squares."""
        board = Board(SPQR_RED)
        self.assertEqual(len(board.board_grid), 7)
        for row in range(7):
            self.assertEqual(len(board.board_grid[row]), 8)

    def test_players_color(self):
        """Test if the input color is the bottom player color and
        opponent player color at top is the opposite (CELTIC_GREEN or SPQR_RED)."""
        board_1 = Board(SPQR_RED)
        self.assertEqual(board_1.bottom_player_color, SPQR_RED)
        self.assertEqual(board_1.top_opponent_color, CELTIC_GREEN)
        board_2 = Board(CELTIC_GREEN)
        self.assertEqual(board_2.bottom_player_color, CELTIC_GREEN)
        self.assertEqual(board_2.top_opponent_color, SPQR_RED)

    def test_number_pieces_left(self):
        """Test if the players start 8 towers and 0 walls."""
        board = Board(SPQR_RED)
        self.assertEqual(board.top_tower_left, 8)
        self.assertEqual(board.top_wall_left, 0)
        self.assertEqual(board.bottom_tower_left, 8)
        self.assertEqual(board.bottom_wall_left, 0)

    def test_pieces_exist_when_board_created(self):
        """Test if there are game pieces on the first and last row on all cells."""
        board = Board(CELTIC_GREEN)
        number_pieces = 0
        for row in range(7):
            for col in range(8):
                if row in (0,6):
                    self.assertIsInstance(board.board_grid[row][col], Piece)
                    number_pieces+=1
            self.assertEqual(number_pieces%8, 0)
        self.assertEqual(number_pieces, 16)

    def test_pieces_with_right_attributes_when_board_created(self):
        """Test if the game pieces are right initialized on the board : right row/col characteristics, right color. """
        board = Board(CELTIC_GREEN)
        for row in range(7):
            for col in range(8):
                if row == 0:
                    self.assertEqual(board.board_grid[row][col].col, col)
                    self.assertEqual(board.board_grid[row][col].row, row)
                    self.assertEqual(board.get_piece(row, col).col, col)
                    self.assertEqual(board.get_piece(row, col).row, row)
                    self.assertEqual(board.board_grid[row][col].color, SPQR_RED)
                    self.assertEqual(board.get_piece(row, col).color, SPQR_RED)
                if row == 6:
                    self.assertEqual(board.board_grid[row][col].col, col)
                    self.assertEqual(board.board_grid[row][col].row, row)
                    self.assertEqual(board.get_piece(row, col).col, col)
                    self.assertEqual(board.get_piece(row, col).row, row)
                    self.assertEqual(board.board_grid[row][col].color, CELTIC_GREEN)
                    self.assertEqual(board.get_piece(row, col).color, CELTIC_GREEN)

    def test_valid_action_initial_towers(self):
        """Test the initial moves that can be played by a tower."""
        board = Board(CELTIC_GREEN)
        moves, sacrifices = board.get_valid_actions(board.get_piece(0,3))
        self.assertEqual(moves, [[(1,2),(2,1)],[(1,3),(2,3)],[(1,4),(2,5)]] )
        self.assertEqual(sacrifices, [] )
        moves, sacrifices = board.get_valid_actions(board.get_piece(6,4))
        self.assertEqual(moves, [[(5,3),(4,2)],[(5,4),(4,4)],[(5,5),(4,6)]] )
        self.assertEqual(sacrifices, [] )

    def test_sacrifice_tower(self):
        """Test if a tower can sacrifice itself to kill an opponent's wall."""
        board = Board(CELTIC_GREEN)
        board.board_grid[3][3] = Piece(3,3,CELTIC_GREEN)
        board.board_grid[3][3].stack_size = 1
        board.board_grid[4][3] = Piece(4, 3, SPQR_RED)
        sacrifices = board.get_valid_actions(board.get_piece(4, 3))[1]
        self.assertEqual(sacrifices, [[(4,3),(3,3)]])

    def test_valid_action_walls(self):
        """Test the valid actions of the walls."""
        board = Board(CELTIC_GREEN)
        board.board_grid[3][3] = Piece(3,3,CELTIC_GREEN)
        board.board_grid[3][3].stack_size = 1
        moves, sacrifices = board.get_valid_actions(board.get_piece(3, 3))
        self.assertEqual(moves, [])
        self.assertEqual(sacrifices, [])

    def test_color_of_get_same_all_color_pieces(self):
        """Test if the method get_all_same_color_pieces() retrieves only pieces of the input color."""
        board = Board(CELTIC_GREEN)
        all_pieces = board.get_all_same_color_pieces(CELTIC_GREEN)
        for piece in all_pieces:
            self.assertEqual(piece.color, CELTIC_GREEN)
        all_pieces = board.get_all_same_color_pieces(SPQR_RED)
        for piece in all_pieces:
            self.assertEqual(piece.color, SPQR_RED)

    def test_recount_towers_walls_left(self):
        """Test if the method get_all_same_color_pieces() retrieves only pieces of the input color."""
        board = Board(CELTIC_GREEN)
        for col in range(8):
            board.board_grid[3][col] = Piece(3,col,CELTIC_GREEN)
            board.board_grid[3][col].stack_size = 1
        nb_towers, nb_walls = board.recount_towers_walls_left(CELTIC_GREEN)
        self.assertEqual(nb_towers, 8)
        self.assertEqual(nb_walls, 8)
        nb_towers, nb_walls = board.recount_towers_walls_left(SPQR_RED)
        self.assertEqual(nb_towers, 8)
        self.assertEqual(nb_walls, 0)

    def test_update_towers_walls_left(self):
        """Test if the method get_all_same_color_pieces() retrieves only pieces of the input color."""
        board = Board(CELTIC_GREEN)
        board.update_towers_walls_left()
        self.assertEqual(board.bottom_tower_left, 8)
        self.assertEqual(board.bottom_wall_left, 0)
        self.assertEqual(board.top_tower_left, 8)
        self.assertEqual(board.top_wall_left, 0)
        for col in range(8):
            board.board_grid[3][col] = Piece(3,col,SPQR_RED)
            board.board_grid[3][col].stack_size = 1
        board.update_towers_walls_left()
        self.assertEqual(board.bottom_tower_left, 8)
        self.assertEqual(board.bottom_wall_left, 0)
        self.assertEqual(board.top_tower_left, 8)
        self.assertEqual(board.top_wall_left, 8)

if __name__ == '__main__':
    unittest.main()
