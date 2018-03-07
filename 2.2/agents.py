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

class Agent():
    def __init__(self, tile_type, game_space):
        self.__tile_type = tile_type 
        self.__game_space = game_space
        self.__nodes_expanded = 0
    def __str__():
        print num expanded and type of agent

class Reflex(Agent):
    def __init__(self, tile_type, game_space):
        super().__init__(self, tile_type, game_space)
        self.__winning_blocks = set( )
        
    def victory_check(self):
        """
        victory_check() -> (int,int)
        
        Check if the agent can win by placing one
        more tile. If so, return the (x,y) position
        of where to place the tile.
        """
        
        # pick the right check for the game we are playing
        if isInstance(self, Gomoku):
            for block in self.__winning_blocks:
                if len(block) == 4
            
        else:
            print('Unknown game. Returning')
            return None
        
class MiniMax(Agent):
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
        
