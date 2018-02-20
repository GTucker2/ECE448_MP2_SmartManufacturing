from copy import deepcopy
from constants import *

""" 
This module defines the Gomoku object.

A Gomoku object is a data structure for 
representing a board of a game of Gomoku.
"""
__author__ = 'Griffin A. Tucker'
__date__ = '2_19_18'

class Gomoku(object):

    def __init__(self, arg = DEFAULT_WIDTH(), h = DEFAULT_HEIGHT()):
        """ 
        __init__(int, int, Gomoku) -> Gomoku

        Initialises a new Gomoku object or inits a
        copy of a preexisting Gomoku object.

        Keyword arguments:
        arg      -- non-specific arg. 
                    the width of the gomoku board or a
                    Gomoku object to copy.
                    defaults to 7. 
        h        -- the height of the gomoku board

        Return a Gomoku object. 
        """
        
        # if instance is of Gomoku class, make a copy
        if isinstance(arg, self.__class__):
            self.__dict__ = deepcopy(arg.__dict__)
        # otherwise define a new object 
        else:
            self.__board_space = [[BLANK_TILE() for x in range(arg)] for y in range(h)]
            self.__blanks = h*w
            self.__width = arg
            self.__height = h

    def set_tile(self, x, y, tile_type):
        """ 
        set_tile(int, int, t in constants.TILE_TYPES()) -> int

        Sets the tile (x,y) of the Gomoku board to
        the value of tile_type. 

        Keyword arguments:
        x         -- the x-coordinate of the tile to set
        y         -- the y-coordinate of the tile to set
        tile_type -- a type to set the tile to (this value
                     must be contained within the array 
                     contants.TILE_TYPES())

        Return 1 if the tile was set successfully; 0 otherwise.  
        """

        # check if we are accessing within range
        if x >= self.__width or x < WIDTH_MIN():
            print('Attempt to access invalid x coordinate; tile not set.')
            return 0
        elif y >= self.__height or y < HEIGHT_MIN():
            print('Attempt to access invalid y coordinate; tile not set.')
            return 0

        # check if setting a known tile type
        if tile_type not in TILE_TYPES():
            print('Invalid tile type; tile not set.')
            return 0

        # if the tile is blank, set the tile to tile_type
        # and decriment the blanks counter, otherwise, 
        # send an error. Can't plance down more than one 
        # stone on a tile. 
        if __board_space[x][y] != BLANK_TILE():
            print('Cant change an occupied tile; tile not set.')
            return 0
        else:
            self.__board_space[x][y] = tile_type;
            self.__blanks -= 1
            return 1
    
    def get_tile(self, x, y):
        """ 
        get_tile(int, int) -> t in constants.TILE_TYPES()

        At the x-y coordinate (x,y), gets the value of
        the Gomoku tile. 

        Keyword arguments:
        x         -- the x-coordinate of the tile to get
        y         -- the y-coordinate of the tile to get

        Return t in constants.TILE_TYPES() stored at
        the requested tile space of the Gomoku object. 
        Return None if invalid (x,y) coordinate specified. 
        """

        # check if we are accessing within range
        if x >= self.__width or x < WIDTH_MIN():
            print('Attempt to access invalid x coordinate; tile not accessed.')
            return None
        elif y >= self.__height or y < HEIGHT_MIN():
            print('Attempt to access invalid y coordinate; tile not accessed.')
            return None
        return self.__board_space[x][y]

    def is_full(self):
        """ 
        is_full() -> int

        Checks if the Gomoku board has any remaining
        blank spaces.

        Keyword arguments:
        None

        Return 1 if there are no more blank spaces on
        the board; otherwise, return 0.
        """
        if self.__blanks <= 0:
            return 1
        else:
            return 0

class __Tile(object):

""" Code below here is to be exclusively used for 
testing the Gomoku class.
"""  
if __name__ == '__main__': 
    new_board = Gomoku(5,5)
    copy_board = Gomoku(new_board)
    new_board.set_tile(1,2,RED_TILE())
    print(new_board.get_tile(1,2))
    print(copy_board.get_tile(1,2))
