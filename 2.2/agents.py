from abc import ABCMeta, abstractmethod
from gomoku import Gomoku
from constants import *

""" 
This module defines the Agent object.

An agent object may be used to play a 
number of game problems. This module 
defines a series of Agent types, i.e.
Reflex, Minimax, and AlphaBeta. 
"""
__author__ = 'Griffin A. Tucker'
__date__ = '3_6_18'

class Agent(metaclass=ABCMeta):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, affinity, game_type, game_space, opponent=None):
        self.__affinity   = affinity
        self.__game_type  = game_type
        self.__game_space = game_space
        self.__in_play    = False
        self.__opponent   = opponent
        if(opponent is not None): self.__opponent.set_opponent(self)

    @abstractmethod 
    def __str__(self): pass
        #print num expanded and type of agent
    
    @abstractmethod
    def make_move(self): pass

    @abstractmethod
    def play_full_game(self): pass

    def get_play_status(self): return self.__in_play
    def get_game_type(self): return self.__game_type
    def get_affinity(self): return self.__affinity 
    def get_game_space(self): return self.__game_space
    def get_opponent(self): return self.__opponent

    def set_play_status(self, status): self.__in_play = status
    def set_opponent(self, opponent): self.__opponent = opponent


class Reflex(Agent):
    def __init__(self, affinity, game_type, game_space, opponent=None):
        super().__init__(affinity, game_type, game_space, opponent)

    def __str__(self):
        pass

    def play_full_game(self): pass


    def make_move(self):

        # If the agent is starting a game, make an 
        # initial move
        if self.get_play_status() == False: 
            self.initial_move()
            return

        # Check wheather the the agent side is going to 
        # win by making one move, make the move
        # OR
        # Check if the oponent has a compromising move 
        best_move = self.victory_check()
        if best_move is None: best_move = self.counter_opponent_win()
        if best_move is None: best_move = self.counter_opponent_adv()
        if best_move is None: best_move = self.best_last_option()
        if best_move != None: 
            x = best_move[0]
            y = best_move[1]
            return self.get_game_space().set_tile(x,y,self.get_affinity())

    def initial_move(self):

        # Make the first move based on the game we
        # are currently playing, otherwise return
        if isinstance(self.get_game_space(), Gomoku):

            # play one stone in the bottom left-hand corner
            self.get_game_space().set_tile(6,0,self.get_affinity())

            # the agents are now in play 
            self.set_play_status(True)
            self.get_opponent().set_play_status(True)

        else:
            print('Unknown game. Returning')
            return None

    def victory_check(self):
        """
        victory_check() -> (int,int)
        
        Check if the agent can win by placing one
        more tile. If so, return the (x,y) position
        of where to place the tile.
        """

        # get essential values
        board = self.get_game_space()
        affinity = self.get_affinity()
        
        # pick the right check for the game we are playing
        if isinstance(board, Gomoku):
            
            possible_wins = board.get_wins(affinity)
            
            if len(possible_wins) == 1: return possible_wins[0]
            elif len(possible_wins) > 1:
                best_win = None
                wins_by_x = {}
                wins_by_y = {}
                for win in possible_wins:
                    if win[0] not in wins_by_x.keys():
                        wins_by_x[win[0]] = []
                    if win[1] not in wins_by_y.keys():
                        wins_by_y[win[1]] = []
                    wins_by_x[win[0]].append(win)
                    wins_by_y[win[1]].append(win)
                for y in wins_by_y:
                    if len(wins_by_y[y]) > 1: 
                        for win in wins_by_y[y]:
                            if best_win is None or win[0] < best_win[0]:
                                best_win = win 
                return best_win

            else: return None

    def counter_opponent_win(self):

         # get essential values
        board = self.get_game_space()
        affinity = self.get_opponent().get_affinity()
        
        # pick the right check for the game we are playing
        if isinstance(board, Gomoku):
            
            possible_wins = board.get_wins(affinity)
            for win in possible_wins:
                print('possible win:'+str(win))
            winning_blocks = board.get_winning_blocks(affinity)
            best_move = None
            for win in possible_wins:
                if best_move is None: best_move = win
                elif win[0] <= best_move[0]: 
                    if win[1] >= best_move[1]:
                        best_move = win
            if best_move is not None: possible_wins.remove(best_move)
            return best_move

            '''for block in winning_blocks[win]:
                    first = block.tiles[0]
                    last = block.tiles[len(block.tiles)-1]
                    if block.direction == 'horizontal':
                        x = first[0] - 1
                        y = first[1]
                        if board.get_tile(x,y) == BLANK_TILE():
                            return (x,y)
                        x = last[0] + 1
                        if board.get_tile(x,y) == BLANK_TILE():
                            return (x,y)
                    elif block.direction == 'vertical':
                        x = first[0] 
                        y = last[1] + 1
                        if board.get_tile(x,y) == BLANK_TILE():
                            return (x,y)
                        y = first[1] - 1
                        if board.get_tile(x,y) == BLANK_TILE():
                            return (x,y)
                    elif block.direction == 'diagonal(\)':
                        x = first[0] - 1
                        y = first[1] - 1
                        if board.get_tile(x,y) == BLANK_TILE():
                            return (x,y)
                        x = last[0] + 1
                        y = last[1] + 1
                        if board.get_tile(x,y) == BLANK_TILE():
                            return (x,y)
                    elif block.direction == 'diagonal(/)':
                        x = first[0] - 1
                        y = first[1] + 1
                        if board.get_tile(x,y) == BLANK_TILE():
                            return (x,y)
                        x = last[0] + 1
                        y = last[1] - 1
                        if board.get_tile(x,y) == BLANK_TILE():
                            return (x,y)
                    else: return None'''

    def counter_opponent_adv(self):

        # get essential values
        board = self.get_game_space()
        affinity = self.get_affinity()
        opaffinity = self.get_opponent().get_affinity()

        # pick the right check for the game we are playing
        if isinstance(board, Gomoku):

            blocks_advn = board.get_adv_blocks(opaffinity)
            for block in blocks_advn:
                print('advantageous block:'+str(block.tiles))
            best_moves = []
            best_move = None

            for block in blocks_advn:
                if block.direction == 'horizontal':
                    x1 = block.tiles[0][0] - 1
                    y1 = block.tiles[0][1] 
                    x2 = block.tiles[2][0] + 1
                    y2 = block.tiles[2][1] 
                    if x1 < 0 or x2 >= 7: return None
                    if board.get_tile(x1,y1) == BLANK_TILE() and \
                    board.get_tile(x2,y2) == BLANK_TILE():
                        best_moves.append((x1,y1))
                elif block.direction == 'vertical':
                    x1 = block.tiles[0][0] 
                    y1 = block.tiles[0][1] - 1 
                    x2 = block.tiles[2][0]
                    y2 = block.tiles[2][1] + 1
                    if y1 < 0 or y2 >= 7: return None
                    if board.get_tile(x1,y1) == BLANK_TILE() and \
                    board.get_tile(x2,y2) == BLANK_TILE():
                        best_moves.append((x2,y2))
                elif block.direction == 'diagonal(\)':
                    x1 = block.tiles[0][0] - 1
                    y1 = block.tiles[0][1] - 1
                    x2 = block.tiles[2][0] + 1
                    y2 = block.tiles[2][1] + 1
                    if x1 < 0 or y1 < 0 or x2 >= 7 or y2 >= 7: return None
                    if board.get_tile(x1,y1) == BLANK_TILE() and \
                    board.get_tile(x2,y2) == BLANK_TILE():
                        best_moves.append((x1,y1))
                elif block.direction == 'diagonal(/)':
                    x1 = block.tiles[0][0] - 1
                    y1 = block.tiles[0][1] + 1
                    x2 = block.tiles[2][0] + 1
                    y2 = block.tiles[2][1] - 1
                    if x1 < 0 or y1 >= 7 or x2 >= 7 or y2 < 0: return None
                    if board.get_tile(x1,y1) == BLANK_TILE() and \
                    board.get_tile(x2,y2) == BLANK_TILE():
                        best_moves.append((x1,y1))

            for move in best_moves:
                print('considered advantageous move:'+str(move))
                if best_move is None: best_move = move 
                elif move[0] < best_move[0] and move[1] == best_move[1]:
                    best_move = move
                elif move[0] == best_move[0] and move[1] > best_move[1]:
                    best_move = move
                elif move[0] < best_move[0] and move[1] > best_move[1]:
                    best_move = move

            return best_move 

    def best_last_option(self): 
        
        # get essential values
        board = self.get_game_space()
        affinity = self.get_affinity()
        
        # pick the right check for the game we are playing
        if isinstance(board, Gomoku):
            
            winning_blocks = board.get_winning_blocks(affinity)
            print('total winning blocks:'+str(len(winning_blocks)))
            best_blocks = []
            best_block = None

            for block in winning_blocks:
                if affinity == BLUE_TILE():
                    if len(best_blocks) == 0: best_blocks.append(block)
                    elif len(block.blue) > len(best_blocks[0].blue):
                        best_blocks = []
                        best_blocks.append(block)
                    elif len(block.blue) == len(best_blocks[0].blue):
                        best_blocks.append(block)
                elif affinity ==RED_TILE():
                    if len(best_blocks) == 0: best_blocks.append(block)
                    if len(block.red) > len(best_blocks[0].red):
                        best_blocks = []
                        best_blocks.append(block)
                    elif len(block.red) == len(best_blocks[0].red):
                        best_blocks.append(block)

            for block in best_blocks:
                print(block.tiles)
                if best_block is None: best_block = block 
                elif block.tiles[0][0] <= best_block.tiles[0][0]: 
                    if (block.tiles[0][1] != block.tiles[1][1]) or \
                    block.tiles[0][1] >= best_block.tiles[0][1]:
                        print('considered block:'+str(block.tiles))
                        best_block = block       
            print('best block:'+str(best_block.tiles))
            best_move = (7,-1)
            for tile_i in range(len(best_block.tiles)):
                tile = best_block.tiles[tile_i]
                next_tile = None
                prev_tile = None 
                if tile_i+1 in range(len(best_block.tiles)):
                    next_tile = best_block.tiles[tile_i+1]
                if tile_i-1 in range(len(best_block.tiles)):
                    prev_tile = best_block.tiles[tile_i-1]
                if board.get_tile(tile[0],tile[1]) == BLANK_TILE():
                    if prev_tile is not None and next_tile is None:
                        if board.get_tile(prev_tile[0],prev_tile[1]) == affinity:
                            if tile[0] <= best_move[0]: 
                                if tile[1] >= tile[1]:
                                    best_move = tile 
                    elif next_tile is not None and prev_tile is None:
                        if board.get_tile(next_tile[0],next_tile[1]) == affinity:
                            if tile[0] <= best_move[0]: 
                                if tile[1] >= tile[1]:
                                    best_move = tile 
                    elif next_tile is not None and prev_tile is not None:
                        if board.get_tile(prev_tile[0],prev_tile[1]) == affinity or \
                        board.get_tile(next_tile[0],next_tile[1]) == affinity:
                            if tile[0] <= best_move[0]: 
                                if tile[1] >= tile[1]:
                                    best_move = tile  
                
            return best_move

'''class MiniMax(Agent):
    def __init__(self, tile_type, game_space, search_depth):
        super().__init__(self, tile_type, game_space)
        self.__search_depth = search_depth
        
class AlphaBeta(Agent):
    def __init__(self, tile_type, game_space, search_depth):
        super().__init__(self, tile_type, game_space)
        self.__search_depth = search_depth
       
class Block(object):
    def __init__(self):
        for tile in tiles:
            self.__tiles.append(tile)
            if tile.get_tile_type == tile_type:
                self.__num_occupied += 1
'''

""" Code below here is to be exclusively used for 
testing the Agent class and its subclasses.
""" 
if __name__ == '__main__': 
    new_game = Gomoku(7,7)

    blue_reflex = Reflex(BLUE_TILE(), Gomoku, new_game)
    red_reflex = Reflex(RED_TILE(), Gomoku, new_game, blue_reflex)
    
    # make the first two assigned moves
    new_game.set_tile(5,1,BLUE_TILE())
    new_game.print_board()
    print('\n')
    new_game.set_tile(1,5,RED_TILE())
    new_game.print_board()
    print('\n')
    blue_reflex.set_play_status(True)
    red_reflex.set_play_status(True)

    # play a full game
    win_status = 0
    while win_status == 0:
        x = input('Make an input to step forward')
        blue_reflex.make_move()
        new_game.print_board()
        if win_status != 0: break 
        else: 
            x = input('Make an input to step forward')
            red_reflex.make_move()
        new_game.print_board()
        print('\n')
