from abc import ABCMeta, abstractmethod
from gomoku import Gomoku
from minimax import MinimaxTree
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
        """ 
        __init__(tile_type, game_type, game_space, Agent) -> Reflex

        Initialises a new Reflex agent, inheriting from a generic Agent.

        Keyword arguments:
        affinity    -- the affinity of this agent
        game_type   -- the Type of the game being played
        game_space  -- the game being played
        opponent    -- the agent this agent is playing against

        Return a Reflex object.
        """
        
        super().__init__(affinity, game_type, game_space, opponent)

    def __str__(self):
        pass

    def play_full_game(self): pass

    def make_move(self):
        """ 
        make_move() -> int

        Makes a move for the reflex agent based on a set
        of rules. 

        Returns -1 if blue wins;
        returns 1 if red wins;
        returns 0 if noone wins. 
        """

        # If the agent is starting a game, make an 
        # initial move
        if self.get_play_status() == False: 
            self.initial_move()
            return

        # for speeds sake, allow the reflex agent to respond to manual
        # input. comment out for automatic running.
        x = int(input('hotwire x:'))
        y = int(input('hotwire y:'))
        return self.get_game_space().set_tile(x,y,self.get_affinity())

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
        """ 
        initial_move() 

        Makes the first move for the agent. 

        Returns nothing.
        """

        # Make the first move based on the game we
        # are currently playing, otherwise return
        if isinstance(self.get_game_space(), Gomoku):

            # play one stone in the bottom left-hand corner
            self.get_game_space().set_tile(0,6,self.get_affinity())

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
            
            # get the possible ways to win
            possible_wins = board.get_wins(affinity)
            
            # if we can win, pick a good win 
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
        """ 
        counter_opponent_win() -> None
        
        Check if the opponent is about to win, and if 
        so, counter that move which they will make.
        """

        # get essential values
        board = self.get_game_space()
        affinity = self.get_opponent().get_affinity()
        
        # pick the right check for the game we are playing
        if isinstance(board, Gomoku):
            
            # get the possible ways for the opponent to win
            possible_wins = board.get_wins(affinity)
            winning_blocks = board.get_winning_blocks(affinity)
            best_move = None

            # sort the best win to counter 
            for win in possible_wins:
                if best_move is None: best_move = win
                elif win[0] <= best_move[0]: 
                    if win[1] >= best_move[1]:
                        best_move = win
            if best_move is not None: possible_wins.remove(best_move)
            return best_move

    def counter_opponent_adv(self):
        """ 
        counter_opponent_adv() -> None
        
        Check if the opponent has a very adventageous
        move, i.e., a row of three tiles with no blockage
        on either end. Counter this.
        """

        # get essential values
        board = self.get_game_space()
        affinity = self.get_affinity()
        opaffinity = self.get_opponent().get_affinity()

        # pick the right check for the game we are playing
        if isinstance(board, Gomoku):

            # get advantageous blocks
            blocks_advn = board.get_adv_blocks(opaffinity)
            best_moves = []
            best_move = None

            # sort the blocks which may be countered
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

            # pick the best move in the best block to counter
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
        """ 
        best_last_option() -> None
        
        Pick a move for the agent to make which is the best 
        based on a set of understood conditions. The best
        move is the most-left, most-low move in the block
        containing the most tiles of the same affinity.
        """
        
        # get essential values
        board = self.get_game_space()
        affinity = self.get_affinity()
        
        # pick the right check for the game we are playing
        if isinstance(board, Gomoku):
            
            # get all possible blocks to make a move in
            winning_blocks = board.get_winning_blocks(affinity)
            print('total winning blocks:'+str(len(winning_blocks)))
            best_blocks = []
            best_block = None

            # find the largest blocks to place a stone in
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

            # find the best block to place a stone in
            for block in best_blocks:
                if best_block is None: best_block = block 
                elif block.tiles[0][0] <= best_block.tiles[0][0]: 
                    if (block.tiles[0][1] != block.tiles[1][1]):
                        if block.direction == 'vertical':
                            if block.tiles[WINNING_ROW_SIZE()-1][1] >= best_block.tiles[WINNING_ROW_SIZE()-1][1]:
                                if affinity == RED_TILE(): 
                                    if len(block.red) >= len(best_block.red):
                                        print('considered block:'+str(block.tiles))
                                        best_block = block    
                                if affinity == BLUE_TILE(): 
                                    if len(block.blue) >= len(best_block.blue):
                                        print('considered block:'+str(block.tiles))
                                        best_block = block
                        else:
                            if block.tiles[0][1] >= best_block.tiles[0][1]:
                                if affinity == RED_TILE(): 
                                    if len(block.red) >= len(best_block.red):
                                        print('considered block:'+str(block.tiles))
                                        best_block = block    
                                if affinity == BLUE_TILE(): 
                                    if len(block.blue) >= len(best_block.blue):
                                        print('considered block:'+str(block.tiles))
                                        best_block = block  
                    else:
                        if block.tiles[0][1] >= best_block.tiles[0][1] and block.tiles[1][0] <= best_block.tiles[1][0]:
                                if affinity == RED_TILE(): 
                                    if len(block.red) >= len(best_block.red):
                                        print('considered block:'+str(block.tiles))
                                        best_block = block    
                                if affinity == BLUE_TILE(): 
                                    if len(block.blue) >= len(best_block.blue):
                                        print('considered block:'+str(block.tiles))
                                        best_block = block       

            # find the best move to make out of the best block 
            # print('best block:'+str(best_block.tiles))
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

class MiniMax(Agent):

    def __init__(self, affinity, game_type, game_space, search_depth, opponent=None):
        """ 
        __init__(tile_type, game_type, game_space, int, Agent) -> MiniMax

        Initializes a minimax agent which inherits from the generic Agent.
        
        Keyword arguments:
        affinity        -- the affinity of this agent
        game_type       -- the Type of the game being played
        game_space      -- the game being played
        search_depth    -- the depth to run the minimax search to
        opponent        -- the agent this agent is playing against

        Return a Minimax object.
        """

        super().__init__(affinity, game_type, game_space, opponent)
        self.__search_depth = search_depth
        self.nodes_expanded = 0

    def __str__(self): pass

    def make_move(self): 
        """ 
        make_move() -> None

        Makes a move for the minimax agent. Runs a search to the
        proper depth and prints the number of nodes expanded. Also
        picks the best move to make based on the search.
        """

        # get relavent information
        affinity = self.get_affinity()
        sample_space = self.get_game_space()
        depth_limit = self.__search_depth

        # run a minimax search and get the best value
        bestval = MinimaxTree.minimax(self, sample_space, affinity, depth_limit, True)
        if bestval[0] is None: bestval = ((0,6),'x', 0)

        # print the number of nodes expanded 
        print(self.nodes_expanded)

        # make the move found by the search 
        self.get_game_space().set_tile(bestval[0][0], bestval[0][1], affinity)

    def play_full_game(self): pass
        
class AlphaBeta(Agent):

    def __init__(self, affinity, game_type, game_space, search_depth, opponent=None):
        """ 
        __init__(tile_type, game_type, game_space, int, Agent) -> MiniMax

        Initializes an alpha-beta agent which inherits from the generic Agent.
        
        Keyword arguments:
        affinity        -- the affinity of this agent
        game_type       -- the Type of the game being played
        game_space      -- the game being played
        search_depth    -- the depth to run the minimax search to
        opponent        -- the agent this agent is playing against

        Return a AlphaBeta object.
        """

        super().__init__(affinity, game_type, game_space, opponent)
        self.__search_depth = search_depth
        self.nodes_expanded = 0

    def __str__(self): pass

    def make_move(self): 
        """ 
        make_move() -> None

        Makes a move for the alpha-beta agent. Runs a search to the
        proper depth and prints the number of nodes expanded. Also
        picks the best move to make based on the search.
        """

        # get relavent information
        affinity = self.get_affinity()
        sample_space = self.get_game_space()
        depth_limit = self.__search_depth

        # run a minimax search and get the best value
        bestval = MinimaxTree.alphabeta(self, sample_space, affinity, depth_limit, -10000, 10001, True)
        if bestval[0] is None: bestval = ((0,6),'x', 0)

        # print the number of nodes expanded 
        print(self.nodes_expanded)

        # make the move found by the search 
        self.get_game_space().set_tile(bestval[0][0], bestval[0][1], affinity)
    
    def play_full_game(self): pass

""" Code below here is to be exclusively used for 
testing the Agent class and its subclasses.
""" 
if __name__ == '__main__': 
    new_game = Gomoku(7,7)

    #blue_reflex = Reflex(BLUE_TILE(), Gomoku, new_game)
    #red_reflex = Reflex(RED_TILE(), Gomoku, new_game, blue_reflex)
    
    blue_alphabeta = AlphaBeta(BLUE_TILE(), Gomoku, new_game, 3)
    #blue_minimax = MiniMax(BLUE_TILE(), Gomoku, new_game, 3)
    red_reflex =  Reflex(RED_TILE(), Gomoku, new_game, blue_alphabeta)

    # make the first two assigned moves
    #new_game.set_tile(1,5,RED_TILE())
    #new_game.print_board()
    #print('\n')
    #new_game.set_tile(5,1,BLUE_TILE())
    #new_game.print_board()
    #print('\n')
    #blue_reflex.set_play_status(True)
    #red_reflex.set_play_status(True)

    # play a full game
    win_status = 0
    while win_status == 0:
        x = input('Make an input to step forward')
        red_reflex.make_move()
        new_game.print_board()
        if win_status != 0: break 
        else: 
            x = input('Make an input to step forward')
            #blue_reflex.make_move()
            #blue_minimax.make_move()
            blue_alphabeta.make_move()
        new_game.print_board()
        print('\n')
