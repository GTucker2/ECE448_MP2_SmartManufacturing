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

    #@abstractmethod
    #def play_full_game(self): pass

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
        best_move = self.victory_check_self()
        if best_move is None: best_move = self.counter_oponent()
        if best_move != None: 
            x = best_move[0]
            y = best_move[1]
            self.get_game_space().set_tile(x,y,self.get_affinity())

        # Check for best possible way to make an 
        # adventageous move
        else: pass

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
        affinity = self.__opponent.get_affinity()
        
        # pick the right check for the game we are playing
        if isinstance(board, Gomoku):
            
            possible_wins = board.get_wins(affinity)
            winning_blocks = board.get_winning_blocks(affinity)
            for win in possible_wins:
                for block in winning_blocks[win]:
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
                        y = first[0] - 1
                        if board.get_tile(x,y) == BLANK_TILE():
                            return (x,y)
                    elif block.direction == 'diagonal(\)':
                        x = first[0] 
                        y = last[1] + 1
                        if board.get_tile(x,y) == BLANK_TILE():
                            return (x,y)
                        y = first[0] - 1
                        if board.get_tile(x,y) == BLANK_TILE():
                            return (x,y)
                    elif block.direction == 'diagonal(/)':
                        x = first[0] 
                        y = last[1] + 1
                        if board.get_tile(x,y) == BLANK_TILE():
                            return (x,y)
                        y = first[0] - 1
                        if board.get_tile(x,y) == BLANK_TILE():
                            return (x,y)
                    else: return None

    def counter_opponent_advantageous(self): pass
    def best_last_option(self): pass
        
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
    blue_reflex.make_move()
