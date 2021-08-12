import pygame
from .constants import SQUARE_SIZE, PADDING, OUTLINE, SPQR_RED, BLACK
pygame.init()

class Piece:
    """
    A class to represent a Murus Gallicus Game between 2 players.

    ...

    Attributes
    ----------
    row : int
        Piece row on the board grid.
    col : int
        Piece column on the board grid.
    color : tuple of int
        RGB color of the owner of the piece.
    direction : array
        Side of the board aimed by the piece; whether 1 or -1.
    x : int
        X / width coordinate of the center of the piece on the game board.
    y : tuple of int
        Y / height coordinate of the center of the piece on the game board.

    Methods
    -------
    calculate_window_position()
        Calculates absolute graphical positive from row and column of the cell where the piece is.
    become_wall()
        Transform a tower / an input piece (double stone) into a wall (simple stone).
    become_tower()
        Transform a wall / an input piece (simple stone) into a tower (double stone).
    draw(window)
        Draws the piece on the graphical window.
    move(row, col)
        Replaces the piece's row and column with the input ones.
    """

    def __init__(self, row, col, color):
        """
        Parameters
        ----------
        row : int
            Row number of the board cell.
        col : int
            Column number of the board cell.
        color
            RGB color of the piece, like (255, 255, 255).
        """
        self.row = row
        self.col = col
        self.color = color
        self.stack_size = 2
        self.x = 0
        self.y = 0
        self.calculate_window_position()

    def calculate_window_position(self):
        """
        Calculates absolute graphical positive from row and column of the cell where the piece is.
        """
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def become_wall(self):
        """
        Transform a tower / an input piece (double stone) into a wall (simple stone).
        """
        self.stack_size = 1

    def become_tower(self):
        """
        Transform a wall / an input piece (simple stone) into a tower (double stone).
        """
        self.stack_size = 2

    def draw(self, window):
        """
        Draws the piece on the graphical window.

        Parameters
        ----------
            window : pygame.Surface
                The pygame graphical window defined among the constants.
        """
        radius = SQUARE_SIZE // 2 - PADDING
        if self.stack_size == 2:
            x1, y1 = self.x - SQUARE_SIZE//8, self.y - SQUARE_SIZE//8
            x2, y2 = self.x + SQUARE_SIZE//8, self.y + SQUARE_SIZE//8
            pygame.draw.circle(window, BLACK, (x1, y1), radius + OUTLINE)
            pygame.draw.circle(window, self.color, (x1, y1), radius)
            pygame.draw.circle(window, BLACK, (x2, y2), radius + OUTLINE)
            pygame.draw.circle(window, self.color, (x2, y2), radius)
        else:
            pygame.draw.circle(window, BLACK, (self.x, self.y), radius + OUTLINE)
            pygame.draw.circle(window, self.color, (self.x, self.y), radius)

    def move(self, row, col):
        """
        Replaces the piece's row and column with the input ones.

        Parameters
        ----------
        row : int
            Row number of the board cell.
        col : int
            Column number of the board cell.
        """
        self.row = row
        self.col = col
        self.calculate_window_position()
