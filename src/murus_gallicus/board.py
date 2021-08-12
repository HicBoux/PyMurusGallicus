import pygame
import math
from .constants import GREY, ROWS, COLS, SOFT_YELLOW, SQUARE_SIZE, CELTIC_GREEN, SPQR_RED
from .piece import Piece
pygame.init()

class Board:
    """
    A class to represent the Murus Gallicus game board.

    ...

    Attributes
    ----------
    board_grid : array
        Array of the cells of the game board.
    selected_piece : None or Piece
        Actual selected piece.
    bottom_player_color : tuple of int
        RGB numbers of the bottom player color, like (255,255,255)
    top_opponent_color : tuple of int
        RGB numbers of the top opponent player color, like (255,255,255).
    bottom_tower_left : int
        Number of bottom player's towers remaining on the game.board
    top_tower_left : int
        Number of top player's towers remaining on the game.board
    bottom_wall_left : int
        Number of bottom player's walls remaining on the game.board
    top_wall_left : int
        Number of top player's walls remaining on the game.board

    Methods
    -------
    determine_opponent_color(bottom_player_color)
        Deduces the top player color from the bottom one
    draw_squares(window)
        Draws the squares on the GUI to build the game board.
    get_piece(row, col)
        Retrieves the piece from a board cell given its row/column coordinates.
    remove_piece(row, col)
        Removes the piece from a board cell given its row/column coordinates.
    move_piece(piece, row, col)
        Moves a piece from its actual board cell to another one with the given row/column coordinates.
    move_tower(piece, next_row_1, next_col_1, next_row_2, next_col_2)
        Distributes a double stone (tower) over the next and upper next cells of the game board.
    def sacrifice_tower(piece, next_row_1, next_col_1)
        Sacrifices a double stone (tower) to remove a simple one (wall) of the opponent on the next cell.
    def create_board(bottom_player_color)
        Initializes the game board and puts all the stone of the 2 players.
    def draw(window)
        Draws the black and white squares which make the grid of the game board, and the stones/pieces on it.
    def get_valid_actions(piece)
        Computes all the valid actions (move, sacrifice) that can be done on the game board by a given piece.
    """

    def __init__(self, bottom_player_color):
        """
        Parameters
        ----------
        bottom_player_color : tuple of int
            RGB numbers of the bottom player color, like (255,255,255).
        """
        self.board_grid = []
        self.selected_piece = None
        self.bottom_player_color = bottom_player_color
        self.top_opponent_color = self.determine_opponent_color(self.bottom_player_color)
        self.create_board(bottom_player_color)
        self.bottom_tower_left = self.top_tower_left = 8
        self.bottom_wall_left = self.top_wall_left = 0

    def determine_opponent_color(self, bottom_player_color):
        """
        Deduces the top player color from the bottom one ;
        it's the opposite color between the 2 possibles.

        Parameters
        ----------
        bottom_player_color : tuple of int
            RGB numbers of the bottom player color, like (255,255,255)

        Returns
        -------
        top_opponent_color : tuple of int
            RGB numbers of the top opponent player color, like (255,255,255).
        """
        if bottom_player_color == SPQR_RED:
            return CELTIC_GREEN
        else:
            return SPQR_RED

    def draw_squares(self, window):
        """
        Draws the squares on the GUI to build the game board.

        Parameters
        ----------
        window : pygame.Surface
            The pygame graphical window defined among the constants.
        """
        window.fill(GREY)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(window, SOFT_YELLOW,
                                 (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def get_piece(self, row, col):
        """
        Retrieves the piece from a board cell given its row/column coordinates.

        Parameters
        ----------
        row : int
            Row number of the board cell.
        col : int
            Column number of the board cell.

        Returns
        -------
        Piece : Piece / int
            If there is one piece on the given cell -> an object of type Piece ;
            else if the cell is empty -> an int.
        """
        return self.board_grid[row][col]

    def remove_piece(self, row, col):
        '''
        Removes the piece from a board cell given its row/column coordinates.

        Parameters
        ----------
        row : int
            Row number of the board cell.
        col : int
            Column number of the board cell.
        '''
        self.board_grid[row][col] = 0

    def move_piece(self, piece, row, col):
        """
        Moves a piece from its actual board cell
        to another one with the given row/column coordinates.

        Parameters
        ----------
        piece : Piece
            Game piece/stone to move.
        row : int
            Row number of the board cell.
        col : int
            Column number of the board cell.
        """
        self.board_grid[piece.row][piece.col], self.board_grid[row][col] = \
            self.board_grid[row][col], self.board_grid[piece.row][piece.col]
        piece.move(row, col)

    def move_tower(self, piece, next_row_1, next_col_1, next_row_2, next_col_2):
        """
        Distributes a double stone (tower) over the next and upper next cells of the game board.

        Parameters
        ----------
        piece : Piece
            Game piece/stone to move.
        next_row_1 : int
            Row number of the first next board cell.
        next_col_1 : int
            Column number of the first next board cell.
        next_row_2 : int
            Row number of the upper next board cell.
        next_col_2 : int
            Column number of the upper next board cell.
        """
        # If the input piece is a double one (tower)
        if piece.stack_size == 2:

            # Remove it from its cell
            self.remove_piece(piece.row, piece.col)

            # Check if there is a piece on the next cell and add one stone (wall)
            next_piece_1 = self.get_piece(next_row_1, next_col_1)
            if next_piece_1 == 0:
                next_piece_1 = Piece(next_row_1, next_col_1, piece.color)
                next_piece_1.stack_size = 1
                self.board_grid[next_row_1][next_col_1] = next_piece_1
            elif next_piece_1.stack_size == 1 and next_piece_1.color == piece.color:
                next_piece_1.stack_size = 2
            else:
                print("!! ERROR : No empty cell or piece of stack size 1 on the way !!")

            # Check if there is a piece on the upper next cell and add one stone (wall)
            next_piece_2 = self.get_piece(next_row_2, next_col_2)
            if next_piece_2 == 0:
                next_piece_2 = Piece(next_row_2, next_col_2, piece.color)
                next_piece_2.stack_size = 1
                self.board_grid[next_row_2][next_col_2] = next_piece_2
            elif next_piece_2.stack_size == 1 and next_piece_2.color == piece.color:
                next_piece_2.stack_size = 2
            else:
                print("!! ERROR : No empty cell or peice of stack size 1 on the way !!")

            self.update_towers_walls_left()


    def sacrifice_tower(self, piece, next_row_1, next_col_1):
        """
        Sacrifices a double stone (tower) to remove a simple one (wall) of the opponent on the next cell.

        Parameters
        ----------
        piece : Piece
            Game piece/stone to move.
        next_row_1 : int
            Row number of the first next board cell.
        next_col_1 : int
            Column number of the first next board cell.
        """
        # Reduce the input tower into a wall
        piece.stack_size = 1
        # Remove the opponent's wall on the next cell
        next_piece_1 = self.get_piece(next_row_1, next_col_1)
        if type(next_piece_1) == Piece:
            self.remove_piece(next_row_1, next_col_1)
            # Update all pieces counts
            if piece.color == self.bottom_player_color:
                self.bottom_tower_left -= 1
                self.bottom_wall_left += 1
                self.top_wall_left -= 1
            elif piece.color == self.top_opponent_color:
                self.top_tower_left -= 1
                self.top_wall_left += 1
                self.bottom_wall_left -= 1
            else:
                print("!! ERROR : The piece's color doesn't match one of both players !!")
        else:
            print("!! ERROR : The drawed circle doesn't seem to designate a piece !!")

        self.update_towers_walls_left()

    def create_board(self, bottom_player_color):
        """
        Initializes the game board and puts all the stone of the 2 players.

        Parameters
        ----------
        bottom_player_color
            RGB numbers of the bottom player color, like (255,255,255)

        """
        if bottom_player_color == SPQR_RED:
            top_opponent_color = CELTIC_GREEN
        else:
            top_opponent_color = SPQR_RED

        for row in range(ROWS):
            self.board_grid.append([])
            for col in range(COLS):
                if row == 0:
                    self.board_grid[row].append(Piece(row, col, top_opponent_color))
                elif row == 6:
                    self.board_grid[row].append(Piece(row, col, bottom_player_color))
                else:
                    self.board_grid[row].append(0)

    def draw(self, window):
        """
        Draws the black and white squares which make the grid of the game board, and the stones/pieces on it.

        Parameters
        ----------
        window : pygame.Surface
            The pygame graphical window defined among the constants.

        """
        self.draw_squares(window)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board_grid[row][col]
                if piece != 0:
                    piece.draw(window)

    def get_valid_actions(self, piece):
        """
        Computes all the valid actions (move, sacrifice) that can be done on the game board by a given piece.

        Parameters
        ----------
        piece : Piece
            Input Piece from where the possible valid actions are computed.

        Returns
        -------
        moves : 2D list of int coordinates
            Coordinates of the next cells where the input piece can be moved.
        sacrifices : 2D list of int coordinates
            Coordinates of the next cells where the input piece can be sacrificed.
        """
        moves = []
        sacrifices = []

        # If the piece doesn't exist ==> return no possible actions
        if piece == 0:
            return moves, sacrifices

        # If the piece is a simple wall ==> no possible actions
        elif piece.stack_size == 1:
            return moves, sacrifices

        # Else ==> the piece is a tower ==> check possible actions
        else:
            row = piece.row
            col = piece.col
            for i in range(-1, 2):
                for j in range(-1, 2):

                    # Avoid moves where the next cell is out of the board
                    if (row+i < 0 or row+i >= ROWS) or (col+j < 0 or col+j >= COLS):
                        pass
                    # Avoid moves where the second next cell is out of the board
                    elif (row+2*i < 0 or row+2*i >= ROWS) or (col+2*j < 0 or col+2*j >= COLS):
                        pass

                    # Ignore actual cell of the piece
                    elif i == 0 and j == 0:
                        pass

                    # if (i!=0 or j!=0)\
                    # and ( (row+i >= 0 and row+i < ROWS) and (col+j > 0 and col+j < COLS) )\
                    # and ( (row+2*i < 0 and row+2*i >= ROWS) and (col+2*j < 0 and col+2*j >= COLS) ):

                    else:

                        next_piece_1 = self.get_piece(row+i, col+j)
                        next_piece_2 = self.get_piece(row+2*i, col+2*j)

                        # Transform cells without piece into a "null" piece of stack_size == 0
                        if type(next_piece_1) == int and next_piece_1 == 0:
                            next_piece_1 = Piece(row+i, col+j, 0)
                            next_piece_1.stack_size = 0
                        if type(next_piece_2) == int and next_piece_2 == 0:
                            next_piece_2 = Piece(row+2*i, col+2*j, 0)
                            next_piece_2.stack_size = 0

                        # Sacrifice on ennemy walls
                        if next_piece_1.color != piece.color and next_piece_1.stack_size == 1:
                            sacrifices.append([(row, col), (row + i, col + j)])

                        # Move a tower on empty cells or same color walls
                        elif ((next_piece_1.color == piece.color or next_piece_1.color == 0) and
                              next_piece_1.stack_size <= 1) \
                                and \
                                ((next_piece_2.color == piece.color or next_piece_2.color == 0) and
                                 next_piece_2.stack_size <= 1):
                            moves.append([(row + i, col + j), (row + 2 * i, col + 2 * j)])

            return moves, sacrifices

    def evaluate(self):
        """
        Evaluate how good is the game situation for the AI player (at the top of the board).

        Returns
        -------
        global_heuristic : float
            The heuristic evaluation score to measure of good is the actual game situation.
        """

        # Evaluate how far from the aim the player is
        own_aim_heuristic = 0
        own_closest_piece_distance = 11
        for piece in self.get_all_same_color_pieces(self.top_opponent_color):
            distance_to_end = math.sqrt( (abs(7-piece.row))**2 + abs((8-piece.col)**2) )
            own_closest_piece_distance = min(own_closest_piece_distance, distance_to_end)
            own_aim_heuristic += distance_to_end
        own_aim_heuristic = 1 / (own_aim_heuristic/56)
        own_closest_piece_distance = (1/own_closest_piece_distance)

        # Evaluate how far from the aim (the top) the bottom player is
        opponent_aim_heuristic = 0
        opponent_closest_piece_distance = 11
        for piece in self.get_all_same_color_pieces(self.bottom_player_color):
            distance_to_end = math.sqrt( abs((0-piece.row))**2 + abs((0-piece.col))**2 )
            opponent_closest_piece_distance = min(opponent_closest_piece_distance, distance_to_end)
            opponent_aim_heuristic += distance_to_end
        opponent_aim_heuristic = 1 / (opponent_aim_heuristic/56)
        opponent_closest_piece_distance =(1/opponent_closest_piece_distance)

        # Evaluate how good your domination is in terms of pieces
        tower_domination_heuristic = (self.top_tower_left - self.bottom_tower_left) * abs((self.top_tower_left - self.bottom_tower_left)) / 64
        # Evaluate how many tower moves remain possible
        towers_left_heuristic = self.top_tower_left**2 / 64
        # Evaluate how many walls you have
        walls_left_heuristic = self.top_wall_left**2 / 64

        # print("H:", own_aim_heuristic, opponent_aim_heuristic, piece_domination_heuristic, towers_left_heuristic)
        # Return a weighted score
        global_heuristic = ( 22 * own_aim_heuristic - 24 * opponent_aim_heuristic
                             + 12 * own_closest_piece_distance - 13 * opponent_closest_piece_distance
                             + 14 * tower_domination_heuristic + 8 * towers_left_heuristic - 7 * walls_left_heuristic)
        # print("G:", global_heuristic)
        return global_heuristic

    def get_all_same_color_pieces(self, color):
        """
        Retrieve into a list all pieces of the input color on the game board.

        Parameters
        ----------
        color : tuple of int
            RGB numbers of the input player color, like (255,255,255)

        Returns
        -------
        same_color_pieces : list of Pieces
            The list of the towers and walls (Pieces) with the input color.
        """
        same_color_pieces = []
        for row in self.board_grid:
            for piece in row:
                if piece != 0 and piece.color == color:
                    same_color_pieces.append(piece)
        return same_color_pieces

    def recount_towers_walls_left(self, color):
        """
        Recount all the towers and walls of the input colors still on the game board.

        Parameters
        ----------
        color : tuple of int
            RGB numbers of the input player color, like (255,255,255)

        Returns
        -------
        nb_towers_left : int
            Number of towers left on the game board.
        nb_walls_left : int
            Number of walls left on the game board.
        """
        all_same_color_pieces = self.get_all_same_color_pieces(color)
        nb_towers_left = 0
        nb_walls_left = 0
        for piece in all_same_color_pieces:
            if piece.stack_size == 2:
                nb_towers_left += 1
            elif piece.stack_size == 1:
                nb_walls_left += 1
        return nb_towers_left, nb_walls_left

    def update_towers_walls_left(self):
        """
        Update the attributes of the Board class which count the number of towers and walls still on the board.
        """
        nb_bottom_towers_left, nb_bottom_walls_left = self.recount_towers_walls_left(self.bottom_player_color)
        self.bottom_tower_left = nb_bottom_towers_left
        self.bottom_wall_left = nb_bottom_walls_left

        nb_top_towers_left, nb_top_walls_left = self.recount_towers_walls_left(self.top_opponent_color)
        self.top_tower_left = nb_top_towers_left
        self.top_wall_left = nb_top_walls_left
