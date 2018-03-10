## author : Michael Racine 
## date: 2/21/18

import Widget
import PlanTree
import priority_queue
import graph
import math

#class that creates the states to go between. 
class State:
    #creates a State object
    #param:  self
    #        name:    the name of the state as a string
    #        dists:   distance to the other states as an array of ints
    #        widgets: The current widgets; this will be a list/dictionary of the widget object
    #return: State object
    def __init__(self, name, dists, widgets):
        self.loc = name
        self.distance_to = dists
        self.vars = widgets
        self.all_done = False

#finds the path with the least number of stops
#param:  start: starting  state for the search
#return: string of path taken
def search_smallest_stops(graph, start, end):
    # Check if the graph is valid. If it is not, return error string.
    if graph is None: return 'graph is null: Function Failed'
    
    # Declare a queue and enqueue the starting node.
    q = priority_queue.PriorityQueue()
    q.put(start, 0)    
    curr_cost = {}
    curr_cost[start] = 0

    # Declare a string to count factory stops
    # Set it to blank space.
    solution = ''
    nodes_expanded = 0

    # While the q is not empty, get the next node on the queue
    # and check for the goal. If at the goal, copy the successful
    # path to the array of mazedata and then return 1. Else,
    # expand the node to the queue. 
    while not q.empty():       
        cur = q.get() 
        nodes_expanded = nodes_expanded + 1
        end[1].add_comp(cur)
        end[2].add_comp(cur)
        end[3].add_comp(cur)
        end[4].add_comp(cur)
        end[5].add_comp(cur)
        if cur != start:
            solution = solution + cur

        if end[1].done and end[2].done and end[3].done and end[4].done and end[5].done:
            return (solution, nodes_expanded)

        for next in graph.neighbors(cur):
            update_cost = curr_cost[cur] + graph.cost(cur, next)
            if next not in curr_cost:
                curr_cost[next] = update_cost
            if update_cost < (curr_cost[next]):
                curr_cost[next] = update_cost
            prior = curr_cost[next] + stop_hist([end[1].next_char,end[2].next_char,end[3].next_char,end[4].next_char,end[5].next_char],next,5)
            q.put(next, prior)          
        
    # Return the failed because solution was not found
    solution = 'FAILED: ' + solution
    return (solution, nodes_expanded)

#finds the path with the least number of stops
#param:  start: starting  state for the search
#return: string of path taken
def search_shortest_dist(graph, start, end):
    # Check if the graph is valid. If it is not, return error string.
    if graph is None: return 'graph is null: Function Failed'
    # Declare a queue and enqueue the starting node.
    q = priority_queue.PriorityQueue()
    q.put(start, 0)        
    curr_cost = {}
    curr_cost[start] = 0

    # Declare a string to count factory stops and int to count miles traversed
    # Set it to blank space.
    solution = ''
    miles_traveled = 0
    nodes_expanded = 0
    # While the q is not empty, get the next node on the queue
    # and check for the goal. If at the goal, return the
    # string of stops and the nodes expanded. Else,
    # expand the node to the queue. 
    while not q.empty():       
        cur = q.get() 
        nodes_expanded = nodes_expanded + 1
        end[1].add_comp(cur)
        end[2].add_comp(cur)
        end[3].add_comp(cur)
        end[4].add_comp(cur)
        end[5].add_comp(cur)
        if cur != start:
            solution = solution + cur
        #the widgets are complete, return
        if end[1].done and end[2].done and end[3].done and end[4].done and end[5].done:
            return (solution, miles_traveled, nodes_expanded)
        #add the neighbors to the queue in order of their cost plus current cost
        for next in graph.neighbors(cur):
            update_cost = curr_cost[cur] + graph.cost(cur, next)
            #if the nighbor isn't in the queue or the new cost is less than it's original cost
            if next not in curr_cost or update_cost < curr_cost[next]:
                curr_cost[next] = update_cost
            prior = update_cost + dist_hist(graph.weights[cur],[end[1].next_char,end[2].next_char,end[3].next_char,end[4].next_char,end[5].next_char],next)
            q.put(next, prior)           
            miles_traveled = miles_traveled + graph.cost(cur, next)
    # Return the failed because solution was not found
    solution = 'FAILED'
    miles_traveled = -1
    return (solution, miles_traveled, nodes_expanded)

#histogram to find the most common component
#param:  comps    : list of the next components to check
#        n        : possible number of components
#        next_comp: the compenent to calculate the cost
#return: component as a string
def stop_hist(comps,next_comp, n):
    num_comp = 5-comps.count(next_comp)
    return num_comp

#histogram to find the shortest distance to a widget
#param:  dist: list of distances to other components
#return: component as a string
def dist_hist(dist, comps, n_comp):
    if dist[n_comp] is 0:
        if comps.count(n_comp):
            return 2000/comps.count(n_comp)
        return 2000
    return dist[n_comp]