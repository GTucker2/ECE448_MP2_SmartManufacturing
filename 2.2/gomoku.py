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

            # general board information
            self.__board_space = [[Tile() for x in range(arg)] for y in range(h)]
            self.__blanks = h*arg
            self.__width = arg
            self.__height = h

            # information for printing to console
            self.__print_space = [['.' for x in range(arg)] for y in range(h)]
            self.blue_chars = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
            self.red_chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
            self.cur_char_red = 0
            self.cur_char_blue = 0
            
            # blocks (5-long tile sets) and adv_blocks (3-long tile
            # sets which are also completely full of the same color
            # tile)
            self.__blocks = self.generate_blocks(WINNING_ROW_SIZE())
            self.__adv_blocks = self.generate_blocks(3)
            self.__adv_blocks_red = []
            self.__adv_blocks_blue = []

            # generate list of blank tiles and blocks
            # which may be uesd to win the game for red and
            # blue
            self.__blank_tiles = []
            self.__winning_blocks_blue = []
            self.__winning_blocks_red = []
            for tile in self.__blocks.keys():
                self.__blank_tiles.append(tile)
                for block in self.__blocks[tile]:
                    if block not in self.__winning_blocks_blue:
                        self.__winning_blocks_blue.append(block)
                    if block not in self.__winning_blocks_red:
                        self.__winning_blocks_red.append(block)

            # moves which would win the game
            self.__wins_red = []
            self.__wins_blue = []

            # blocks which are being used in play and moves
            # which should be considered by the minimax and alpha
            # beta searches. This minimizes the state space and 
            # speeds up runtime 
            self.active_blocks = []
            self.viable_moves = []

    # This set of getter functions returns valid information
    # for a given tile type or a given tile 
    def get_blocks(self, tile): return self.__blocks[tile]
    def get_adv_blocks(self, affinity):
        if affinity == RED_TILE(): return self.__adv_blocks_red
        elif affinity == BLUE_TILE(): return self.__adv_blocks_blue
        else: return None
    def get_winning_blocks(self, affinity):
        if affinity == RED_TILE(): 
            return self.__winning_blocks_red
        elif affinity == BLUE_TILE(): 
            return self.__winning_blocks_blue
        else: return None
    def get_wins(self, affinity):
        if affinity == RED_TILE(): return self.__wins_red
        elif affinity == BLUE_TILE(): return self.__wins_blue
        else: return None
    def get_blanks(self): return self.__blank_tiles

    def generate_blocks(self, size):
        """ 
        generate_blocks(int) -> [blocks]

        Generates all possible blocks of length size
        in the Gomoku board.

        Keyword arguments:
        size -- the size of the block to generate

        Return an array of blocks present in the board.
        """

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
                    new_block = Block(tiles,'horizontal')
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
                    new_block = Block(tiles,'vertical')
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
                    new_block = Block(tiles,'diagonal(/)')
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
                    new_block = Block(tiles,'diagonal(/)')
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
                    new_block = Block(tiles,'diagonal(\)')
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
                    new_block = Block(tiles,'diagonal(\)')
                    for tile in tiles:
                        if tile not in blocks.keys(): blocks[tile] = []
                        blocks[tile].append(new_block)

        return blocks 

    def update_blocks(self, x, y, affinity):
        """ 
        update_blocks(int, int, tile_type) -> None

        Updates all the blocks in the Gomoku board 
        affected by the move made to tile (x,y)

        Keyword arguments:
        x        -- the x coordinate of a move being made
        y        -- the y coordinate of a move being made 
        affinity -- the tile_type of a move being made

        Return nothing. 
        """

        # for every block in the board associated 
        # with the tile (x,y)
        for block in self.__blocks[(x,y)]:

            # record the block as being used if it has
            # not been prior
            if block not in self.active_blocks: 
                self.active_blocks.append(block)
            
            # if we are placing a red tile
            if affinity == RED_TILE():

                # remove this block from the possible wins for blue
                if block in self.__winning_blocks_blue:
                    self.__winning_blocks_blue.remove(block)

                # update the tile info associated with the block
                block.red.append((x,y))
                block.blank.remove((x,y))

                # save this block as a possible win if it sets us up for one
                if len(block.blank) == 1 and len(block.red) == WINNING_ROW_SIZE() - 1:
                    l = len(block.tiles) - 1
                    xw1 = block.tiles[0][0]
                    yw1 = block.tiles[0][1]
                    xw2 = block.tiles[l][0]
                    yw2 = block.tiles[l][1]
                    if self.get_tile(xw1,yw1) == BLANK_TILE() or self.get_tile(xw2,yw2) == BLANK_TILE():
                        self.__wins_red.append(block.blank[0]) 
            
            # if we are placing a blue tile
            elif affinity == BLUE_TILE():

                # remove this block from the possible wins for red
                if block in self.__winning_blocks_red:
                    self.__winning_blocks_red.remove(block)

                # update the tile info associated with the block
                block.blue.append((x,y))
                block.blank.remove((x,y))

                # save this block as a possible win if it sets us up for one
                if len(block.blank) == 1 and len(block.blue) == WINNING_ROW_SIZE() - 1:
                    l = len(block.tiles) - 1
                    xw1 = block.tiles[0][0]
                    yw1 = block.tiles[0][1]
                    xw2 = block.tiles[l][0]
                    yw2 = block.tiles[l][1]
                    if self.get_tile(xw1,yw1) == BLANK_TILE() or self.get_tile(xw2,yw2) == BLANK_TILE():
                        self.__wins_blue.append(block.blank[0])

            # otherwise do nothing as we cannot remove a tile
            elif affinity == BLANK_TILE():
                print('cannot remove a tile')

    def update_adv_blocks(self, x, y, affinity):
        """ 
        update_adv_blocks(int, int, tile_type) -> None

        Updates all the advantageous blocks in the 
        Gomoku board affected by the move made to 
        tile (x,y) 

        Keyword arguments:
        x        -- the x coordinate of a move being made
        y        -- the y coordinate of a move being made 
        affinity -- the tile_type of a move being made

        Return nothing. 
        """

        # for every block in the board associated 
        # with the tile (x,y)
        for block in self.__adv_blocks[(x,y)]:

            # update the tile info associated with the block
            block.blank.remove((x,y)) 

            # if we are placing a red tile
            if affinity == RED_TILE(): 
                block.red.append((x,y))
                if len(block.red) == 3:
                    self.__adv_blocks_red.append(block)

            # if we are placing a blue tile
            elif affinity == BLUE_TILE(): 
                block.blue.append((x,y))
                if len(block.blue) == 3:
                    self.__adv_blocks_blue.append(block)
            
            else: print('cannot remove a tile')

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
        if self.get_tile(x,y) != BLANK_TILE():
            print('Tile occupied: override values')
            x = int(input('enter a default x:'))
            y = int(input('enter a default y:'))
            if y < 0: return 0
        if x >= self.__width or x < WIDTH_MIN():
            print('Attempt to access invalid x coordinate; tile not set.')
            x = int(input('enter a default x:'))
            y = int(input('enter a default y:'))
            if x < 0: return 0
        elif y >= self.__height or y < HEIGHT_MIN():
            print('Attempt to access invalid y coordinate; tile not set.')
            x = int(input('enter a default x:'))
            y = int(input('enter a default y:'))
            if y < 0: return 0

        # add viable moves for minimax; viable moves are all tiles surrounding
        # the tile
        if (x,y) in self.viable_moves: self.viable_moves.remove((x,y))
        viable_blue = False
        viable_red = False
        moves_to_add = [(x-1,y),(x+1,y),(x-1,y-1),(x-1,y+1),(x+1,y-1),(x+1,y+1),(x,y+1),(x,y-1)]
        for move in moves_to_add:
            if move[0] >= 0 and move[0] < 7 and move[1] >= 0 and move[1] < 7:
                if move not in self.viable_moves and self.get_tile(move[0],move[1]) == BLANK_TILE():
                    for block in self.get_winning_blocks(RED_TILE()):
                        if move in block.tiles: viable_red = True 
                    for block in self.get_winning_blocks(BLUE_TILE()):
                        if move in block.tiles: viable_blue = True
                    if viable_red is True and viable_blue is True:  
                        self.viable_moves.append(move)

        # Adjust the type of tile, decriment the blanks counter, and 
        # remove from the list of remaining possible moves
        if self.__board_space[x][y].change_type(tile_type) == 0: return 0
        self.__blank_tiles.remove((x,y))
        if tile_type == RED_TILE(): 
            self.__print_space[x][y] = self.red_chars[self.cur_char_red]
            self.cur_char_red += 1
        else: 
            self.__print_space[x][y] = self.blue_chars[self.cur_char_blue]
            self.cur_char_blue += 1
        self.__blanks -= 1
        self.update_blocks(x,y,tile_type)
        self.update_adv_blocks(x,y,tile_type)

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
            print('Attempt to access invalid x coordinate; tile not accessed:'+str((x,y)))
            return None
        elif y >= self.__height or y < HEIGHT_MIN():
            print('Attempt to access invalid y coordinate; tile not accessed:'+str((x,y)))
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

        for y in range(0, self.__height):
            for x in range(0, self.__width):
                print(self.__print_space[x][y], end='')
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
            if y < 0: return 0

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

    def __init__(self, tiles, direction):
        self.direction = direction
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
