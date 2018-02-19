from constants import *

class Gomoku(object):
    def __init__(w, h):
        self.__board_space = Gomoku.generate_board(w, h)
        self.__width = w
        self.__height = h
        
    def set_tile(self, x, y, tile_type):
        # check if we accessing within range
        if x >= self.__width or x < WIDTH_MIN:
            print('Attempt to access invalid x coordinate; tile not set.')
            return 0
        elif y >= self.__height or y < HEIGHT_MIN:
            print('Attempt to access invalid y coordinate; tile not set.')
            return 0
        # check if setting a known tile type
        if tile_type in ACCEPTED_NAMES_RED:
            set_type = RED_TILE
        elif tile_type in ACCEPTED_NAMES_BLUE:
            set_type = BLUE_TILE
        else:
            print('Invalid tile type; tile not set.')
            return 0
        self.__board_space[x][y] = set_type
        return 1
    
    def get_tile(self, x, y):
        # check if we accessing within range
        if x >= self.__width or x < WIDTH_MIN:
            print('Attempt to access invalid x coordinate; tile not accessed.')
            return None
        elif y >= self.__height or y < HEIGHT_MIN:
            print('Attempt to access invalid y coordinate; tile not accessed.')
            return None
        return __board_space[x][y]
        
    def generate_board(w, h):
        new_board = [];
        for collumn_i in range(0,w):
            new_board[collumn_i] = []
            for row_i in range(0,h):
                new_board[collumn_i][row_i] = BLANK_TILE
        
