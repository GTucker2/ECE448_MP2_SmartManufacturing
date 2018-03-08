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
    q.put(root, 0)    
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

        if end[1].done and end[2].done and end[3].done and end[4].done and end[5].done:
            return (solution, nodes_expanded)

        for next in graph.neighbors(cur):
            update_cost = curr_cost[cur] + graph.cost(cur, next)
            if update_cost < curr_cost.get(next, math.inf):
                curr_cost[next] = update_cost
                prior = update_cost + stop_hist(end)  #THIS DOESN'T WORK YET
                q.put(next, prior)                    #"""""""""""""""""""""
                end[1].add_comp(next)
                end[2].add_comp(next)
                end[3].add_comp(next)
                end[4].add_comp(next)
                end[5].add_comp(next)
                solution = solution + cur
        
    # Return the failed because solution was not found
    solution = 'FAILED'
    return (solution, nodes_expanded)

#finds the path with the least number of stops
#param:  start: starting  state for the search
#return: string of path taken
def search_shortest_dist(graph, start, end):
    # Check if the graph is valid. If it is not, return error string.
    if graph is None: return 'graph is null: Function Failed'
    # Declare a queue and enqueue the starting node.
    q = priority_queue.PriorityQueue()
    q.put(root, 0)        

    # Declare a string to count factory stops and int to count miles traversed
    # Set it to blank space.
    solution = ''
    miles_traveled = 0
    nodes_expanded = 0
    # While the q is not empty, get the next node on the queue
    # and check for the goal. If at the goal, copy the successful
    # path to the array of mazedata and then return 1. Else,
    # expand the node to the queue. 
    while not q.empty():       
        cur = q.get() 
        nodes_expanded = nodes_expanded + 1

        if end[1].done and end[2].done and end[3].done and end[4].done and end[5].done:
            return (solution, miles_traveled, nodes_expanded)

        for next in graph.neighbors(cur):
            update_cost = curr_cost[cur] + graph.cost(cur, next)
            if update_cost < curr_cost.get(next, math.inf):
                curr_cost[next] = update_cost
                prior = update_cost + dist_hist(end)  #THIS DOESN'T WORK YET
                q.put(next, prior)                    #"""""""""""""""""""""
                end[1].add_comp(next)
                end[2].add_comp(next)
                end[3].add_comp(next)
                end[4].add_comp(next)
                end[5].add_comp(next)
                solution = solution + cur
                miles_traveled = miles_traveled + graph.cost(cur, next)
    # Return the failed because solution was not found
    solution = 'FAILED'
    miles_traveled = -1
    return (solution, miles_traveled, nodes_expanded)

#histogram to find the most common component
#param:  comps: list of the next components to check
#return: component as a string
def stop_hist(comps):
    best = 'A'
    if(comps.count(best) < comps.count('B')):
        best='B'
    if(comps.count(best) < comps.count('C')):
        best='C'
    if(comps.count(best) < comps.count('D')):
        best='D'
    if(comps.count(best) < comps.count('E')):
        best='E'
    return best

#histogram to find the shortest distance to a widget
#param:  dist: list of distances to other components
#return: component as a string
def dist_hist(dist):
    short = dist['A']
    if(short > dist['B']):
        short = dist['B']
    if(short > dist['C']):
        short = dist['C']
    if(short > dist['D']):
        short = dist['D']
    if(short > dist['E']):
        short = dist['E']
    return short