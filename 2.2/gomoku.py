from copy import deepcopy
from constants import *

""" 
This module defines the Gomoku object.

A Gomoku object is a data structure for 
representing a board of a game of Gomoku.
"""
__author__ = 'Griffin A. Tucker'
__date__ = '3_6_18'

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
            self.__board_space = [[Tile() for x in range(arg)] for y in range(h)]
            self.__blanks = h*arg
            self.__width = arg
            self.__height = h
            self.__blocks = self.generate_blocks(WINNING_ROW_SIZE())
            self.__winning_blocks_red = [block for block in self.__blocks]
            self.__winning_blocks_blue = [block for block in self.__blocks]

    def generate_blocks(self, size):

        # create the blocks map
        blocks = {}

        # generate horizontal blocks 
        for y in range (0, self.__height):
            tiles = []
            for x in range(0, self.__width):
                if len(tiles) != size:
                    tiles.append((x,y))
                else:
                    tiles.remove((tiles[0]))
                    tiles.append((x,y))
                if len(tiles) == size:
                    new_block = Block(tiles)
                    for tile in tiles:
                        if tile not in blocks.keys(): blocks[tile] = []
                        blocks[tile].append(new_block)

        # generate vertical blocks
        for x in range(0, self.__width):
            tiles = []
            for y in range(0, self.__height):
                if len(tiles) != size:
                    tiles.append((x,y))
                else:
                    tiles.remove(tiles[0])
                    tiles.append((x,y))
                if len(tiles) == size:
                    new_block = Block(tiles)
                    for tile in tiles:
                        if tile not in blocks.keys(): blocks[tile] = []
                        blocks[tile].append(new_block)

        # generate diagonal blocks
        # credit @Squidcor here: https://stackoverflow.com/questions/6150382/c-process-2d-array-elements-in-a-diagonal-fashion
        #First half (including middle diagonal)
        for i in range(0,self.__width):
            tiles = []
            for j in range(0,i+1):
                if len(tiles) != size:
                    tiles.append((j,i-j))
                else:
                    tiles.remove(tiles[0])
                    tiles.append((j,i-j))
                if len(tiles) == size:
                    new_block = Block(tiles)
                    for tile in tiles:
                        if tile not in blocks.keys(): blocks[tile] = []
                        blocks[tile].append(new_block)
        #Second half (excluding middle diagonal) 
        N = self.__width
        for i in reversed(range(0, N)):
            tiles = []
            for j in range(0,i):
                if len(tiles) != size:
                    tiles.append((N-i+j,N-j-1))
                else:
                    tiles.remove(tiles[0])
                    tiles.append((N-i+j,N-j-1))
                if len(tiles) == size:
                    new_block = Block(tiles)
                    for tile in tiles:
                        if tile not in blocks.keys(): blocks[tile] = []
                        blocks[tile].append(new_block)

        # generate diagonal blocks (other way)
        #First half (including middle diagonal)
        N = self.__width - 1
        for i in range(0,N+1):
            tiles = []
            for j in range(0,i+1):
                if len(tiles) != size:
                    tiles.append((i-j, N-j))
                else:
                    tiles.remove(tiles[0])
                    tiles.append((i-j, N-j))
                if len(tiles) == size:
                    new_block = Block(tiles)
                    for tile in tiles:
                        if tile not in blocks.keys(): blocks[tile] = []
                        blocks[tile].append(new_block)
        #Second half (excluding middle diagonal) 
        N = self.__width
        for i in reversed(range(0, N-1)):
            tiles = []
            for j in range(0,i+1):
                if len(tiles) != size:
                    tiles.append((N-j-1,i-j))
                else:
                    tiles.remove(tiles[0])
                    tiles.append((N-j-1,i-j))
                if len(tiles) == size:
                    new_block = Block(tiles)
                    for tile in tiles:
                        if tile not in blocks.keys(): blocks[tile] = []
                        blocks[tile].append(new_block)

        return blocks 

    def update_blocks(self, x, y, affinity):
        for block in self.__blocks[(x,y)]:
            if affinity == RED_TILE():
                if block in self.__winning_blocks_blue:
                    remove(block)
                block.red.append((x,y))
                block.blank.remove((x,y))
            elif affinity == BLUE_TILE():
                if block in self.__winning_blocks_red:
                    remove(block)
                block.blue.append((x,y))
                block.blank.remove((x,y))
            elif affinity == BLANK_TILE():
                print('cannot remove a tile')
            print('Tile Accessed: ' + str((x,y)))
            print('Block altered: ' + str(block.tiles))
            print('Reds: ' + str(block.red))
            print('Blues: ' + str(block.blue))
            print('Blanks: ' + str(block.blank))
            print('\n')

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

        Return 1 if setting the tile won the game for red.
        Returns -1 if setting the tile won the game for blue.
        Returns 0 if setting the tile did nothing.  
        """

        # check if we are accessing within range
        if x >= self.__width or x < WIDTH_MIN():
            print('Attempt to access invalid x coordinate; tile not set.')
            return 0
        elif y >= self.__height or y < HEIGHT_MIN():
            print('Attempt to access invalid y coordinate; tile not set.')
            return 0

        # Adjust the type of tile, decriment the blanks counter, and 
        # remove from the list of remaining possible moves
        self.__board_space[x][y].change_type(tile_type)
        self.__blanks -= 1
        self.update_blocks(x,y,tile_type)
        #self.__moves.remove(x,y)

        # Gather the neighbors of the tile
        neighbors = {}
        if (x-1) >= WIDTH_MIN():  neighbors['W'] = self.__board_space[x-1][y]
        if (y-1) >= HEIGHT_MIN(): neighbors['S'] = self.__board_space[x][y-1]
        if (x+1) < self.__width:  neighbors['E'] = self.__board_space[x+1][y]
        if (y+1) < self.__height: neighbors['N'] = self.__board_space[x][y+1]
        if (x-1) >= WIDTH_MIN() and (y+1) < self.__height: 
            neighbors['NW'] = self.__board_space[x-1][y+1]
        if (x-1) >= WIDTH_MIN() and (y-1) >= HEIGHT_MIN(): 
            neighbors['SW'] = self.__board_space[x-1][y-1]
        if (x+1) < self.__width and (y+1) < self.__height: 
            neighbors['NE'] = self.__board_space[x+1][y+1]
        if (x+1) < self.__width and (y-1) >= HEIGHT_MIN(): 
            neighbors['SE'] = self.__board_space[x+1][y-1]

        # check for win condition
        if self.__board_space[x][y].find_friends(neighbors) == 1:
            if tile_type == RED_TILE(): return 1
            else: return -1
        else: return 0
    
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
    
    def print_board(self):
        """
        print_board() -> int

        Iterates through the board space and prints
        the data to console. Useful for testing.

        Keyword arguments:
        None

        Returns 1 is successful. Otherwise returns 0.
        """

        for x in range(0, self.__width):
            for y in range(0, self.__height):
                print(self.__board_space[x][y].get_tile_type(), end='')
            print('\n', end='')

class Tile(object):

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
        self.__vertical_friends = set([self])
        self.__horizontal_friends = set([self])
        self.__rightdiag_friends = set([self])
        self.__leftdiag_friends = set([self])

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
            self.__tile_type = tile_type
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
        # tile_tyle is the type of the tile being evaluated
        tile_type = self.__tile_type

        # Check the neighbors of the tile for friendly pieces.
        # Union the friend sets of the tile is there are friends.
        # This block of code is disgusting and unreadable. I apologise.
        for k in neighbors.keys():
            if k == 'SE' and neighbors['SE'].get_tile_type() == tile_type: 
                neighbors['SE'].__rightdiag_friends = neighbors['SE'].__rightdiag_friends.union(self.__rightdiag_friends)
                self.__rightdiag_friends = self.__rightdiag_friends.union(neighbors['SE'].__rightdiag_friends)
                max_friends.append(len(self.__rightdiag_friends))
            
            elif k == 'NW' and neighbors['NW'].get_tile_type() == tile_type: 
                neighbors['NW'].__rightdiag_friends = neighbors['NW'].__rightdiag_friends.union(self.__rightdiag_friends)
                self.__rightdiag_friends = self.__rightdiag_friends.union(neighbors['NW'].__rightdiag_friends)
                max_friends.append(len(self.__rightdiag_friends)) 
            
            elif k == 'N' and neighbors['N'].get_tile_type() == tile_type: 
                neighbors['N'].__vertical_friends = neighbors['N'].__vertical_friends.union(self.__vertical_friends)
                self.__vertical_friends = self.__vertical_friends.union(neighbors['N'].__vertical_friends)
                max_friends.append(len(self.__vertical_friends)) 
            
            elif k == 'S' and neighbors['S'].get_tile_type() == tile_type:
                neighbors['S'].__vertical_friends = neighbors['S'].__vertical_friends.union(self.__vertical_friends)
                self.__vertical_friends = self.__vertical_friends.union(neighbors['S'].__vertical_friends)
                max_friends.append(len(self.__vertical_friends)) 
            
            elif k == 'W' and neighbors['W'].get_tile_type() == tile_type: 
                neighbors['W'].__horizontal_friends = neighbors['W'].__horizontal_friends.union(self.__horizontal_friends)
                self.__horizontal_friends = self.__horizontal_friends.union(neighbors['W'].__horizontal_friends)
                max_friends.append(len(self.__horizontal_friends)) 
            
            elif k == 'E' and neighbors['E'].get_tile_type() == tile_type: 
                neighbors['E'].__horizontal_friends = neighbors['E'].__horizontal_friends.union(self.__horizontal_friends)
                self.__horizontal_friends = self.__horizontal_friends.union(neighbors['E'].__horizontal_friends)
                max_friends.append(len(self.__horizontal_friends)) 
            
            elif k == 'NE' and neighbors['NE'].get_tile_type() == tile_type: 
                neighbors['NE'].__leftdiag_friends = neighbors['NE'].__leftdiag_friends.union(self.__leftdiag_friends)
                self.__leftdiag_friends = self.__leftdiag_friends.union(neighbors['NE'].__leftdiag_friends)
                max_friends.append(len(self.__leftdiag_friends)) 
            
            elif k == 'SW' and neighbors['SW'].get_tile_type() == tile_type:
                neighbors['SW'].__leftdiag_friends = neighbors['SW'].__leftdiag_friends.union(self.__leftdiag_friends) 
                self.__leftdiag_friends = self.__leftdiag_friends.union(neighbors['SW'].__leftdiag_friends)
                max_friends.append(len(self.__leftdiag_friends)) 

        # If any of the tile's friend sets length >= the length of
        # a winning row of friends, return win; otherwise return not_win
        if len(max_friends) > 0 and max(max_friends) >= WINNING_ROW_SIZE(): return 1
        else: return 0

class Block(object):

    def __init__(self, tiles):
        self.tiles = [tile for tile in tiles]
        self.red = []
        self.blue = []
        self.blank = [tile for tile in tiles] 

""" Code below here is to be exclusively used for 
testing the Gomoku class.
"""  
if __name__ == '__main__': 
    new_board = Gomoku(7,7)
    copy_board = Gomoku(new_board)
    new_board.set_tile(1,2,RED_TILE())
    new_board.set_tile(0,2,RED_TILE())
    new_board.set_tile(2,2,RED_TILE())
    new_board.set_tile(3,2,RED_TILE())
    print(new_board.set_tile(4,2,RED_TILE()))
    new_board.print_board()
