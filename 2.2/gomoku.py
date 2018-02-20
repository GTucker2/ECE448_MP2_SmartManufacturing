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
            self.__board_space = [[__Tile() for x in range(arg)] for y in range(h)]
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

        # Adjust the type of tile and decriment the blanks counter
        self.__board_space[x][y].change_type(tile_type)
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
        return self.__board_space[x][y].get_tile_type()

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

    def __init__(self):
        """ 
        __init__() -> __Tile

        Initialises a new __Tile object. New tiles
        are always initialized as blanks. 

        Keyword arguments:
        None

        Return a __Tile object. 
        """
        self.__tile_type = BLANK_TILE()
        self.__vertical_friends = Set([self])
        self.__horizontal_friends = Set([self])
        self.__rightdiag_friends = Set([self])
        self.__leftdiag_friends = Set([self])

    def get_tile_type(self):
        """ 
        get_tile_type() -> t in constants.TYLE_TYPES()

        Returns the type of the current tile as an
        int; 0 = blank, 1 = red, -1 = blue.

        Keyword arguments:
        None

        Returns the type of the tile.
        """
        return self.__tile_type

    def change_type(self, tile_type):
        """ 
        change_type(t in constants.TILE_TYPES()) -> int

        Sets the tile type of the tile to the given 
        value unless it is currentlly some value other
        than that of BLANK_TILE().

        Keyword arguments:
        tile_type -- a numeric value representing the type
                     of tile this tile is; 0 for blank,
                     1 for red, and -1 for blue.

        Returns 1 if successful and 0 otherwise.
        """

        # Check if we are attempting to remove a tile
        if tile_type == BLANK_TILE():
            print('Cant remove a stone from the board; tile not set.')
            return 0
        # Check if the tile is currently occupied
        if self.__tile_type != BLANK_TILE():
            print('Cant change an occupied tile; tile not set.')
            return 0

        # Set the new tile type if it is valid, otherwise fail
        if tile_type in TILE_TYPES():
            self.tile_type = tile_type
            return 1
        else: 
            return 0

    def find_friends(self, neighbors):
        """ 
        find_friends(__Tile[]) -> int

        Given the surrounding tiles, i.e. the neighbors,
        this function poles them to see if they are 
        friends (of the same tile_type). If they are, 
        it unions their respective relationship sets with 
        those of the calling tile. If a set with a length 
        of more than that of the winning condition is 
        ormed, the function returns a win flag.

        Keyword arguments:
        neighbors -- a dictionary of the surrounding 
                     tiles following the following map:

                        NW   |   N   |   NE   
                     --------|-------|--------
                        W    |  ici  |   E
                     --------|-------|--------
                        SW   |   S   |   SE

                    Where 'ici' is the calling tile and the
                    labels of the squares are keys to the
                    dictionary. 

        Return 1 if a set of friends is created  with a 
        length greater than the set winning condition.
        Otherwise return 0.
        """

        # max_friends stores the lengths of all created friend sets
        max_friends = []

        # create lambda functions for calculating horizontile, vertical, right-
        # diagonal, and left-diagonal friend sets.
        h = lambda x: len(x.__horizontal_friends.union(self.__horizontal_friends))
        v = lambda x: len(x.__vertical_friends.union(self.__vertical_friends))
        r = lambda x: len(x.__rightdiag_friends.union(self.__rightdiag_friends))
        l = lambda x: len(x.__leftdiag_friends.union(self.__leftdiag_friends))

        # Check the neighbors of the tile for friendly pieces.
        # Union the friend sets of the tile is there are friends.
        if (NW = neighbors[NW()].get_tile_type()) == tile_type: max_friends.append(r(SE)) 
        if (N = neighbors[N()].get_tile_type()) == tile_type: max_friends.append(v(N)) 
        if (S = neighbors[S()].get_tile_type()) == tile_type: max_friends.append(v(S)) 
        if (W = neighbors[W()].get_tile_type()) == tile_type: max_friends.append(h(W)) 
        if (E = neighbors[E()].get_tile_type()) == tile_type: max_friends.append(h(E)) 
        if (NE = neighbors[NE()].get_tile_type()) == tile_type: max_friends.append(l(NE)) 
        if (SW = neighbors[SW()].get_tile_type()) == tile_type: max_friends.append(l(SW)) 

        # If any of the tile's friend sets length >= the length of
        # a winning row of friends, return win; otherwise return not_win
        if max(max_friends) >= WINNING_ROW(): return 1
        else: return 0

""" Code below here is to be exclusively used for 
testing the Gomoku class.
"""  
if __name__ == '__main__': 
    new_board = Gomoku(5,5)
    copy_board = Gomoku(new_board)
    new_board.set_tile(1,2,RED_TILE())
    print(new_board.get_tile(1,2))
    print(copy_board.get_tile(1,2))
