import pygame
pygame.init()

FPS = 60
WIDTH, HEIGHT = 800, 700
ROWS, COLS = 7, 8
SQUARE_SIZE = HEIGHT//ROWS

# GRAPHICAL USER INTERFACE
ICON_PATH = './src/murus_gallicus/assets/noun_checkers_1684698.png'
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

PADDING = 20
OUTLINE = 2

# RGB COLORS
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CLEAR_BLUE = (102, 178, 255)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
SOFT_YELLOW = (246, 233, 195)
SOFT_RED = (244, 129, 134)
CELTIC_GREEN = (1, 135, 73)
DARK_GREEN = (14, 79, 0)
SPQR_RED = (213, 28, 31)
DARK_RED = (140, 8, 2)

P_2_Minimax = "Player VS MiniMax AI"
P_2_P = "Player vs Player"
AI_MINIMAX_DEPTH = 3
