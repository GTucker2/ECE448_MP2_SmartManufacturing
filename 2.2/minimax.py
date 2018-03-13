from gomoku import *
from constants import *

""" 
This module defines the MinimaxTree object.

A MinimaxTree object may be used to perform 
the minimax algorithm on a given samplespace
"""
__author__ = 'Griffin A. Tucker'
__date__ = '3_12_18'

class MinimaxTree():
    
    def minimax(agent, sample_space, affinity, depth_limit, maxi, this_move=None): 
        """ 
        minimax(Agent, Gomoku, tile_type, int, bool, (int,int)) -> ((int,int), int, int)

        Runs the minimax algorithm on a given sample space up to a given depth.

        Keyword arguments:
        agent           -- the agent using this algorithm
        sample_space    -- the game we are playing on 
        affinity        -- the tile_type of this level of the algorithm
        depth_limit     -- the depth to search to
        maxi            -- if the current level is max or min
        this_move       -- the move associated with this node

        Return a tuple of node information (the best move
        to perform according to the search as well as the node
        value of that best move)
        """

        # get the viable moves after the node made at this node is made
        possible_moves = sample_space.viable_moves

        # if we are at a leaf node, return the heuristic value of the node,
        # otherwise, run the search on its children
        if depth_limit == 0: return (this_move, MinimaxNode.h(Gomoku(sample_space), affinity, this_move[0], this_move[1]), 0)
        else: 

            # gget the relavent data for the next level
            if affinity == RED_TILE(): next_affinity = BLUE_TILE()
            else: next_affinity = RED_TILE()

            #Either maximize or minimize based on the level, and recurse
            if maxi is True:
                best_value = (None,-10000, 0)
                for move in possible_moves:
                    agent.nodes_expanded += 1
                    v = MinimaxTree.minimax(agent, Gomoku(sample_space), next_affinity, depth_limit-1, False, move)
                    max_val = max(best_value[1], v[1])
                    if max_val != best_value[1]:
                        best_value = v 
                best_value = (best_value[0], best_value[1])
                return best_value
            else:
                best_value = (None,10001,0)
                for move in possible_moves:
                    agent.nodes_expanded += 1
                    v = MinimaxTree.minimax(agent, Gomoku(sample_space), next_affinity, depth_limit-1, True, move)
                    min_val =  min(best_value[1], v[1])
                    if min_val != best_value[1]:
                        best_value = v
                best_value = (best_value[0], best_value[1])
                return best_value
    
class MinimaxNode(object):

    def get_value(): return self.__value 

    def h(sample_space, affinity, x, y):
        """ 
        h(Gomoku, tile_type, int, int) -> int

        Calculates a value for the minimax algorithm
        based on a set of understood pattern difficulties

        Keyword arguments:
        sample_space    -- the game being played
        affinity        -- the affinity of the tile being evaluated
        x               -- the x of the tile being evaluated
        y               -- the y of the tile being evaluated

        Return the evaluated score. 
        """

        # if this move wins the game do not return max score
        if (x,y) in sample_space.get_wins(affinity): return 10000

        #elif affinity == BLUE_TILE(): sample_space.set_tile(x,y,affinity) != 0: return 10000

        # get essential values
        blocks = sample_space.get_blocks((x,y))
        possible_blocks = []
        score = 0

        for block in blocks:
            if block in sample_space.active_blocks:
                possible_blocks.append(block)

        # Evaluate all winning blocks
        for block in possible_blocks:
            # get essential info
            if affinity == RED_TILE(): eval_list = block.red
            elif affinity == BLUE_TILE(): eval_list = block.blue
            first = 0
            last = WINNING_ROW_SIZE()-1

            # 4-blocks with no blocked ends: max_score
            # 4-blocks with one blocked end: 500
            if len(eval_list) == 4: 
                if sample_space.get_tile(block.tiles[first][0],block.tiles[first][1]) == BLANK_TILE():
                    
                    if block.direction == 'horizontal':
                        xw = block.tiles[last][0] + 1
                        yw = block.tiles[last][1]
                    elif block.direction == 'vertical':
                        xw = block.tiles[last][0] 
                        yw = block.tiles[last][1] + 1
                    elif block.direction == 'diagonal(\)':
                        xw = block.tiles[last][0] + 1
                        yw = block.tiles[last][1] + 1
                    else:
                        xw = block.tiles[last][0] - 1
                        yw = block.tiles[last][1] + 1
                    if (xw >= 0 or xw < 7 or yw >= 0 or yw < 7) and sample_space.get_tile(xw,yw) == BLANK_TILE(): 
                        return 10000
                    else: score += 100
                elif sample_space.get_tile(block.tiles[last][0],block.tiles[last][1]) == BLANK_TILE():
                    if block.direction == 'horizontal':
                        xw = block.tiles[first][0] - 1
                        yw = block.tiles[first][1]
                    elif block.direction == 'vertical':
                        xw = block.tiles[first][0] 
                        yw = block.tiles[first][1] - 1
                    elif block.direction == 'diagonal(\)':
                        print(block.tiles)
                        xw = block.tiles[first][0] - 1
                        yw = block.tiles[first][1] - 1
                    else:
                        print(block.tiles)
                        xw = block.tiles[first][0] + 1
                        yw = block.tiles[first][1] - 1
                    if (xw < 0 or xw >= 7 or yw < 0 or yw >= 7) or sample_space.get_tile(xw,yw) == BLANK_TILE(): 
                        return 10000
                    else: score += 100
                else: score += 80

            # 1-blocks with no blocked ends: 10
            # 1-blocks with one blocked end: 5
            # 2-blocks with no blocked ends: 40
            # 2-blocks with one blocked end: 20
            # 3-blocks with no blocked ends: 80
            # 3-blocks with one blocked end: 60
            else:
                if sample_space.get_tile(block.tiles[first][0],block.tiles[first][1]) != BLANK_TILE():
                    if block.direction == 'horizontal':
                        xw = block.tiles[first][0] - 1
                        yw = block.tiles[first][1]
                    elif block.direction == 'vertical':
                        xw = block.tiles[first][0] 
                        yw = block.tiles[first][1] - 1
                    elif block.direction == 'diagonal(\)':
                        xw = block.tiles[first][0] - 1
                        yw = block.tiles[first][1] - 1
                    else:
                        xw = block.tiles[first][0] - 1
                        yw = block.tiles[first][1] + 1
                    if (xw < 0 or xw >= 7 or yw < 0 or yw >= 7) or sample_space.get_tile(xw,yw) != BLANK_TILE(): 
                        if len(eval_list) == 3: score += 10
                        elif len(eval_list) == 2: score += 5
                        else: score += 1
                elif sample_space.get_tile(block.tiles[last][0],block.tiles[last][1]) != BLANK_TILE():
                    if block.direction == 'horizontal':
                        xw = block.tiles[last][0] + 1
                        yw = block.tiles[last][1]
                    elif block.direction == 'vertical':
                        xw = block.tiles[last][0] 
                        yw = block.tiles[last][1] + 1
                    elif block.direction == 'diagonal(\)':
                        xw = block.tiles[last][0] + 1
                        yw = block.tiles[last][1] + 1
                    else:
                        xw = block.tiles[last][0] + 1
                        yw = block.tiles[last][1] - 1
                    if (xw < 0 or xw >= 7 or yw < 0 or yw >= 7) or sample_space.get_tile(xw,yw) != BLANK_TILE(): 
                        if len(eval_list) == 3: score += 10
                        elif len(eval_list) == 2: score += 5
                        else: score += 1
                else: 
                    if len(eval_list) == 3: score += 20
                    elif len(eval_list) == 2: score += 10
                    else: score += 1
        
        return score 
                
                