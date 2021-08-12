from copy import deepcopy
import random
import pygame

class MinimaxAI:
    """
    A class to represent the Minimax AI to play against a human player.

    ...

    Attributes
    ----------
    initial_depth : int
        Depth of the MiniMax trees generated each time the AI computes the best action to play.

    Methods
    -------
    play_minimax(board, depth, max_player, game)
        Executes the MiniMax algorithm to compute the best action to play for the AI.
    simulate_action(piece, action, temp_board)
        Simulates an action of an input piece and returns the associated board.
    simulate_all_valid_actions(board, color, game)
        Retrieves in a list of simulated boards all the possible actions that can be played
        by a given player on a given board.
    draw_moves(game, board, piece)
        Draws on the board the actions checked by the AI during the execution of the MiniMax algorithm.
    """
    def __init__(self, depth):
        """
        Parameters
        ----------
        depth : int
            Tree depth of the Minimax Algorithm.
        """
        self.initial_depth = depth

    def play_minimax(self, board, depth, max_player, game):
        """
        Executes the MiniMax algorithm to compute the best action to play for the AI.

        Parameters
        ----------
        board : Board
            Game board.
        depth : int
            Tree depth of the MiniMax Algorithm.
        max_player : bool
            True if the AI player is simulated, False if it's the other.
        game : Game
            Murus Gallicus Game.

        Returns
        -------
        max_min_eval : int
            Heuristic quality evaluation score which estimates how good the game situation for the player is.
        best_action : Board
            Simulated game board containing the best action to play.
        """
        if depth == 0 or (game.check_if_over() and game.winner != 0):
            return board.evaluate(), board

        elif max_player:
            max_eval = float('-inf')
            best_action = None
            all_valid_actions = self.simulate_all_valid_actions(board, game.board.top_opponent_color)
            random.shuffle(all_valid_actions) # Remove the shuffling if the minimax deapth increases
            for action in all_valid_actions:
                evaluation = self.play_minimax(action, depth-1, False, game)[0]
                max_eval = max(max_eval, evaluation)
                if max_eval == evaluation:
                    best_action = action
            return max_eval, best_action

        else:
            min_eval = float('inf')
            best_action = None
            all_valid_actions = self.simulate_all_valid_actions(board, game.board.bottom_player_color)
            random.shuffle(all_valid_actions) # Remove the shuffling if the minimax deapth increases
            for action in all_valid_actions:
                evaluation = self.play_minimax(action, depth-1, True, game)[0]
                min_eval = min(min_eval, evaluation)
                if min_eval == evaluation:
                    best_action = action
            return min_eval, best_action

    @staticmethod
    def simulate_action(piece, action, temp_board):
        """
        Simulates an action of an input piece and returns the associated board.

        Parameters
        ----------
        piece : Piece
            Game piece : wall or tower.
        action : list of tuples
            List of tuple of row/col coordinates representing the action to play.
        temp_board :
            Temporary game board upon which to simulate the input action.

        Returns
        -------
            temp_board :
                Temporary game board upon which was simulated the input action.
        """
        # If the input action is a tower sacrifice
        if action[0] == (piece.row, piece.col):
            next_row, next_col = action[1][0], action[1][1]
            temp_board.sacrifice_tower(piece, next_row, next_col)
        # Else : if the input action is a tower move
        else:
            next_row_1, next_col_1 = action[0][0], action[0][1]
            next_row_2, next_col_2 = action[1][0], action[1][1]
            temp_board.move_tower(piece, next_row_1, next_col_1, next_row_2, next_col_2)
        return temp_board

    def simulate_all_valid_actions(self, board, color):
        """
        Retrieves in a list of simulated boards all the possible actions that can be played
        by a given player on a given board.

        Parameters
        ----------
        board
        color : tuple of int
            RGB numbers of the input player color, like (255,255,255)

        Returns
        -------
        all_simulated_boards : List of Boards
             List of temporary game boards with each time a different played action among all the possible valid ones.
        """
        all_simulated_boards = []

        for piece in board.get_all_same_color_pieces(color):
            moves, sacrifices = board.get_valid_actions(piece)
            valid_actions = moves
            valid_actions.extend(sacrifices)
            for action in valid_actions:
                #draw_moves(game, board, piece)
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                new_board = self.simulate_action(temp_piece, action, temp_board)
                all_simulated_boards.append(new_board)

        return all_simulated_boards

    @staticmethod
    def draw_moves(game, board, piece):
        """
        Draws on the board the actions checked by the AI during the execution of the MiniMax algorithm.

        Parameters
        ----------
        game : Game
            Murus Gallicus Game.
        board : Board
            Game board.
        piece : Piece
            Game piece.
        """
        all_valid_actions = board.get_valid_actions(piece)
        board.draw(game.window)
        pygame.draw.circle(game.window, (0,255,0), (piece.x, piece.y), 50, 5)
        game.draw_valid_actions(all_valid_actions)
        pygame.display.update()
        #pygame.time.delay(30)


