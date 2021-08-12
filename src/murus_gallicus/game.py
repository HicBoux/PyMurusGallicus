import pygame
from .constants import SQUARE_SIZE, SPQR_RED, CELTIC_GREEN, CLEAR_BLUE, BLUE
from .board import Board
pygame.init()

class Game:
    """
    A class to represent a Murus Gallicus Game between 2 players.

    ...

    Attributes
    ----------
    selected : None or Game
        Actual selected item.
    board : Board
        Game board.
    turn : tuple of int
        RGB color of the player to play now.
    valid_actions : array
        All possible actions that can played.
    window : pygame.Surface
        The pygame graphical window defined among the constants.
    winner : tuple of int
        RGB color of the player who has won.

    Methods
    -------
    update()
        Deduces the top player color from the bottom one
    init(bottom_player_color)
        Initializes the game situation like in the rules of Murus Gallicus.
    reset()
        Reinitializes the game situation like in the rules of Murus Gallicus.
    select(row, col)
        Selects the input item and move it as wished, or reset the selected attribute.
    move(row, col)
        Moves the selected item as wished if it's possible.
    change_turn()
        Changes the game turn : the other player has to play now.
    def draw_valid_actions(all_valid_actions)
        Draws circles where there are possible actions to do with the actual selected piece.
    check_if_over()
        Checks all pieces on the board in order to know if one of the 2 player has won or lost,
        and so if the game is over.
    get_board()
        Retrieve the attribute "board" of the class Game.
    ai_move(board)
        Update game board and switch turn to next player.
    """

    def __init__(self, window, bottom_player_color):
        """
        Parameters
        ----------
        window : pygame.Surface
            The pygame graphical window defined among the constants.
        bottom_player_color : tuple of int
            RGB numbers of the bottom player color, like (255,255,255)
        """
        self.selected = None
        self.board = Board(bottom_player_color)
        self.turn = SPQR_RED
        self.valid_actions = []
        self.window = window
        self.is_over = False
        self.winner = 0

    def update(self):
        """
        Updates the game situation.
        """
        self.board.draw(self.window)
        self.draw_valid_actions(self.valid_actions)
        pygame.display.update()

    def init(self, bottom_player_color):
        """
        Initializes the game situation like in the rules of Murus Gallicus.

        Parameters
        ----------
        bottom_player_color : tuple of int
            RGB numbers of the bottom player color, like (255,255,255)
        """
        self.selected = None
        self.board = Board(bottom_player_color)
        self.turn = SPQR_RED
        self.valid_actions = {}
        self.is_over = False
        self.winner = 0

    def reset(self, bottom_player_color):
        """
        Reinitializes the game situation like in the rules of Murus Gallicus.

        Parameters
        ----------
        bottom_player_color : tuple of int
            RGB numbers of the bottom player color, like (255,255,255)
        """
        self.init(bottom_player_color)

    def select(self, row, col):
        """
        Selects the input item and move it as wished, or reset the selected attribute.

        Parameters
        ----------
        row : int
            Row number of the board cell.
        col : int
            Column number of the board cell.
        """
        if self.selected:
            result = self.move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        else:
            piece = self.board.get_piece(row, col)
            if piece != 0 and piece.color == self.turn:
                self.selected = piece
                self.valid_actions = self.board.get_valid_actions(piece)
                return True

        return False

    def move(self, row, col):
        """
        Moves the selected item as wished if it's possible.

        Parameters
        ----------
        row : int
            Row number of the board cell.
        col : int
            Column number of the board cell.
        """
        all_moves = self.valid_actions[0]
        all_sacrifices = self.valid_actions[1]
        if self.selected and any((row, col) in coordinates for coordinates in all_moves):
            move_to_do = [move for move in all_moves if (row, col) in move][0]
            next_row_1, next_col_1 = move_to_do[0][0], move_to_do[0][1]
            next_row_2, next_col_2 = move_to_do[1][0], move_to_do[1][1]
            self.board.move_tower(self.selected, next_row_1, next_col_1, next_row_2, next_col_2)
            self.change_turn()
        elif self.selected and any((row, col) in coordinates for coordinates in all_sacrifices):
            sacrifice_to_do = [move for move in all_sacrifices if (row, col) in move][0]
            next_row_1, next_col_1 = sacrifice_to_do[1][0], sacrifice_to_do[1][1]
            self.board.sacrifice_tower(self.selected, next_row_1, next_col_1)
            self.change_turn()
        else:
            return False

        return True

    def change_turn(self):
        """
        Changes the game turn : the other player has to play now.
        """
        self.valid_actions = []
        self.selected = None
        if self.turn == SPQR_RED:
            self.turn = CELTIC_GREEN
        else:
            self.turn = SPQR_RED

    def draw_valid_actions(self, all_valid_actions):
        """
        Draws circles where there are possible actions to do with the actual selected piece.

        Parameters
        ----------
        all_valid_actions
            All possible actions that can played.
        """
        if len(all_valid_actions) > 0:
            for move in all_valid_actions[0]:
                row, col = move[1]
                x, y = SQUARE_SIZE * col + SQUARE_SIZE // 2, SQUARE_SIZE * row + SQUARE_SIZE // 2
                pygame.draw.circle(self.window, BLUE, (x, y), 15)
            for sacrifice in all_valid_actions[1]:
                row, col = sacrifice[1]
                x, y = SQUARE_SIZE * col + SQUARE_SIZE // 2, SQUARE_SIZE * row + SQUARE_SIZE // 2
                pygame.draw.circle(self.window, CLEAR_BLUE, (x, y), 15)

    def check_if_over(self):
        """
        Checks all pieces on the board in order to know if one of the 2 player has won or lost,
        and so if the game is over.

        Returns
        -------
        is_game_over : bool
            True if there's a game over situation, False otherwise.
        """
        # Retrieve all walls and tower of both players
        all_bottom_pieces = self.board.get_all_same_color_pieces(self.board.bottom_player_color)
        all_top_pieces = self.board.get_all_same_color_pieces(self.board.top_opponent_color)

        # Check if one of the 2 players has won

        # For the player at the bottom of the board
        nb_possible_actions = 0
        for piece in all_bottom_pieces:
            moves, sacrifices = self.board.get_valid_actions(piece)
            nb_possible_actions += len(moves) + len(sacrifices)
            # The player has won if one of its pieces has reached the end of the board
            if piece.row == 0:
                self.is_over = True
                self.winner = self.board.bottom_player_color
                return True
        # The player has lost if he has no action no play
        if nb_possible_actions == 0:
            self.is_over = True
            self.winner = self.board.top_opponent_color
            return True

        # For the player at the top of the board
        nb_possible_actions = 0
        for piece in all_top_pieces:
            moves, sacrifices = self.board.get_valid_actions(piece)
            nb_possible_actions += len(moves) + len(sacrifices)
            # The player has won if one of its pieces has reached the end of the board
            if piece.row == 6:
                self.is_over = True
                self.winner = self.board.top_opponent_color
                return True
        # The player has lost if he has no action no play
        if nb_possible_actions == 0:
            self.is_over = True
            self.winner = self.board.bottom_player_color
            return True

        # Otherwise it means there isn't a winner yet
        return False


    def get_board(self):
        """
        Retrieve the attribute "board" of the class Game.

        Returns
        -------
        board : Board
            Game board.
        """
        return self.board

    def ai_move(self, board):
        """
        Update game board and switch turn to next player.

        Parameters
        ----------
        board : Board
            Game board.
        """
        self.board = board
        self.change_turn()
