import pygame
from .constants import FPS, HEIGHT, WIDTH, SQUARE_SIZE, WINDOW
from .constants import BLACK, WHITE, CLEAR_BLUE, BLUE, SOFT_YELLOW, \
    CELTIC_GREEN, DARK_GREEN, SPQR_RED, DARK_RED, AI_MINIMAX_DEPTH, P_2_P, P_2_Minimax, ICON_PATH
from .game import Game
from .minimax import MinimaxAI
pygame.init()

class UIRender:
    """
    A class to represent the Graphical User Interface (GUI) of the game.

    ...

    Attributes
    ----------
    run : boolean
        Indicates if the GUI is running.
    clock : pygame.time.Clock
        Indicates the GUI time since it has started.
    game_mode : str
        Game mode : Player vs Player, Player vs MiniMax etc...
    bottom_player_color :
        RGB numbers of the bottom player color, like (255,255,255)

    Methods
    -------
    set_window_icon(image_path)
        Sets the pygame window icon.
    get_row_col_from_mouse(pos)
        Retrieves the row and column of the cell from the mouse position.
    display_game_over(winner_color)
        Displays the game over menu / screen.
    display_title(window, font, text, color, position)
        Displays a title / text on the graphical window.
    button(window, font, text, color, position, hover_color, event=None, action=None, *actions_args)
        Displays a clickable button on the graphical window.
    launch()
        Starts the graphical window and displays the first screen / menu / page.
    choose_player_color()
        Displays the screen / menu where you have to choose your side/color.
    display_game_over(winner_color)
        Displays the screen / menu where the winner of the game is shown and where you can choose to play again.
    start_game(bottom_player_color)
        Displays the in game screen / menu.
    """
    def __init__(self, image_path=ICON_PATH):
        """
        Parameters
        ----------
        row : int
            Row number of the board cell.
        col : int
            Column number of the board cell.
        color
            RGB color of the player starting bottom, like (255, 255, 255).
        """
        self.run = True
        self.clock = pygame.time.Clock()
        self.game_mode = "UNKNOWN"
        self.bottom_player_color = 0
        self.top_player_color = 0
        import os
        print(os.getcwd() )
        print(image_path)
        self.set_window_icon(image_path)
        pygame.display.set_caption('Murus Gallicus')

    def set_window_icon(self, image_path):
        """
        Sets the pygame window icon.

        Parameters
        ----------
        image_path : str
            Path to the image.
        """
        pygame.init()
        icon_surface = pygame.image.load(image_path)
        pygame.display.set_icon(icon_surface)

    def set_bottom_player_color(self, bottom_player_color):
        self.bottom_player_color = bottom_player_color
        if bottom_player_color == SPQR_RED:
            self.top_player_color = CELTIC_GREEN
        else:
            self.top_player_color = SPQR_RED

    def get_row_col_from_mouse(self, pos):
        """
        Retrieves the row and column of the cell from the mouse position.

        Parameters
        ----------
        pos : tuple of int
            X / Y actual coordinates of the mouse on the window.
        """
        x, y = pos
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        return row, col

    def display_game_over(self, winner_color):
        """
        Displays the game over menu / screen.

        Parameters
        ----------
        winner_color : tuple of int
            RGB color of the winner of the game, like (255, 255, 255).
        """
        pygame.init()
        font = pygame.font.Font(None, 70)
        if winner_color == SPQR_RED:
            text = font.render("Romans win !", True, BLUE)
        elif winner_color == CELTIC_GREEN:
            text = font.render("Gauls win !", True, BLUE)
        else:
            text = font.render("!!! Error : romans nor gauls have won !!!", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 4))
        WINDOW.blit(text, text_rect)
        pygame.display.update()

    def display_title(self, window, font, text, color, position):
        """
        Displays a title / text on the graphical window.
        Parameters
        ----------
        window : pygame.Surface
            The pygame graphical window defined among the constants.
        font : pygame.font.Font
            The font to use for the text to display.
        text : str
            Text to display.
        color :
            RGB color of the text to display.
        position : tuple of int
            Position of the text on the graphical window.
        """
        pygame.init()
        text = font.render(text, True, color)
        text_rect = text.get_rect(center=position)
        window.blit(text, text_rect)

    def button(self, window, font, text, color, position, hover_color, event=None, action=None, *actions_args):
        """
        Displays a clickable button on the graphical window.

        Parameters
        ----------
        window : pygame.Surface
            The pygame graphical window defined among the constants.
        font : pygame.font.Font
            The font to use for the text to display.
        text : str
            Text to display.
        color :
            RGB color of the text to display by default.
        position : tuple of int
            Position of the text on the graphical window.
        hover_color : tuple of int
            RGB color of the text to display when the mouse is hovering it.
        event : pygame.event.EventType
            Pygame event like mouse click or move.
        action
            Method to execute.
        actions_args
            *Args of the method "action" to execute.

        Returns
        -------

        """
        text_render = font.render(text, True, color)
        text_render_hover = font.render(text, True, hover_color)
        text_rect = text_render.get_rect(center=position)
        window.blit(text_render, text_rect)

        if text_rect.collidepoint(pygame.mouse.get_pos()):  # Check if the button has been clicked
            window.blit(text_render_hover, text_rect)
            # Check if event is of type pygame.event and if action is a function that can be executed
            if isinstance(event, pygame.event.EventType) and event.button == 1 and callable(action):
                action(*actions_args)

    def launch(self):
        """
        Starts the graphical window and displays the first screen / menu / page.
        """
        pygame.init()
        while self.run:

            self.clock.tick(FPS)
            WINDOW.fill(SOFT_YELLOW)

            font = pygame.font.Font(None, 70)
            self.display_title(WINDOW, font, "Py Murus Gallicus", SPQR_RED, (WIDTH / 2, HEIGHT / 8))

            font = pygame.font.Font(None, 40)
            self.display_title(WINDOW, font, "Please choose your game mode :", BLACK, (WIDTH / 2, HEIGHT / 4))

            self.button(WINDOW, font, P_2_P, CLEAR_BLUE, (WIDTH / 2, 1.5 * HEIGHT / 4), BLUE, None, None,
                        None)
            self.button(WINDOW, font, P_2_Minimax, CLEAR_BLUE, (WIDTH / 2, 2 * HEIGHT / 4), BLUE, None, None,
                        None)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.button(WINDOW, font, P_2_P, CLEAR_BLUE, (WIDTH / 2, 1.5 * HEIGHT / 4), BLUE,
                                event, self.choose_player_color, P_2_P)
                    self.button(WINDOW, font, P_2_Minimax, CLEAR_BLUE, (WIDTH / 2, 2 * HEIGHT / 4), BLUE,
                                event, self.choose_player_color, P_2_Minimax)

            pygame.display.update()

    def choose_player_color(self, game_mode):
        """
        Displays the screen / menu where you have to choose your side/color.
        """
        pygame.init()
        while self.run:
            self.clock.tick(FPS)
            WINDOW.fill(SOFT_YELLOW)

            font = pygame.font.Font(None, 40)
            self.display_title(WINDOW, font, "Please choose your team :", BLACK, (WIDTH / 2, HEIGHT / 4))

            self.button(WINDOW, font, "Gauls", CELTIC_GREEN, (WIDTH / 2, 1.5 * HEIGHT / 4), DARK_GREEN, None, None)
            self.button(WINDOW, font, "Romans", SPQR_RED, (WIDTH / 2, 2 * HEIGHT / 4), DARK_RED, None, None)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.button(WINDOW, font, 'Gauls', CELTIC_GREEN, (WIDTH / 2, 1.5 * HEIGHT / 4), DARK_GREEN,
                                event, self.start_game, game_mode, CELTIC_GREEN)
                    self.button(WINDOW, font, 'Romans', SPQR_RED, (WIDTH / 2, 2 * HEIGHT / 4), DARK_RED,
                                event, self.start_game, game_mode, SPQR_RED)

            pygame.display.update()

    def display_game_over(self, winner_color):
        """
        Displays the screen / menu where the winner of the game is shown and where you can choose to play again.

        Parameters
        ----------
        winner_color : tuple of int
            RGB color of the winner of the game, like (255, 255, 255).
        """
        pygame.init()
        while self.run:
            self.clock.tick(FPS)

            font = pygame.font.Font(None, 70)
            self.button(WINDOW, font, "Click here to restart", CLEAR_BLUE, (WIDTH / 2, 3.5 * HEIGHT / 8),
                        BLUE, None, None)

            if winner_color == SPQR_RED:
                self.display_title(WINDOW, font, "Romans win !", SPQR_RED, (WIDTH / 2, 2.5 * HEIGHT / 8))
            elif winner_color == CELTIC_GREEN:
                self.display_title(WINDOW, font, "Gauls win !", CELTIC_GREEN, (WIDTH / 2, 2.5 * HEIGHT / 8))
            else:
                self.display_title(WINDOW, font, "!!! Error : romans nor gauls have winned !!!", BLACK,
                                   (WIDTH / 2, 2.5 * HEIGHT / 8))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.button(WINDOW, font, "Click here to restart", CLEAR_BLUE, (WIDTH / 2, 3.5 * HEIGHT / 8),
                                BLUE, event, self.launch)

            pygame.display.update()

    def start_game(self, game_mode, bottom_player_color):
        """
        Displays the in game screen / menu.

        Parameters
        ----------
        bottom_player_color : tuple of int
            RGB color of the player starting bottom, like (255, 255, 255).
        """
        pygame.init()
        game = Game(WINDOW, bottom_player_color)
        self.set_window_icon(ICON_PATH)
        self.set_bottom_player_color(bottom_player_color)

        while self.run:
            self.clock.tick(FPS)

            if game_mode == P_2_Minimax and game.turn == self.top_player_color:
                    ai = MinimaxAI(AI_MINIMAX_DEPTH)
                    eval_value, new_board = ai.play_minimax(game.get_board(), ai.initial_depth, self.top_player_color, game)
                    game.ai_move(new_board)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_row_col_from_mouse(pos)
                    game.select(row, col)

            game.update()

            game.check_if_over()
            if game.is_over:
                if game.winner == CELTIC_GREEN:
                    self.display_game_over(CELTIC_GREEN)
                else:
                    self.display_game_over(SPQR_RED)


        pygame.quit()
