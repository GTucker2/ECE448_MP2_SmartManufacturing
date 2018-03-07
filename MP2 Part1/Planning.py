## author : Michael Racine 
## date: 2/21/18

import queue
import Widget
import PlanTree

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
    q = queue.Queue()         
    q.enqueue(root)    

    # Declare a string to count factory stops
    # Set it to blank space.
    solution = ''
    nodes_expanded = 0

    # While the q is not empty, get the next node on the queue
    # and check for the goal. If at the goal, copy the successful
    # path to the array of mazedata and then return 1. Else,
    # expand the node to the queue. 
    while q.size() > 0:       
        cur = q.dequeue() 
        if cur.traversed is False:
            #TODO: create search 
            cur.traversed = True
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
    q = queue.Queue()         
    q.enqueue(root)    

    # Declare a string to count factory stops and int to count miles traversed
    # Set it to blank space.
    solution = ''
    miles_traveled = 0
    nodes_expanded = 0
    # While the q is not empty, get the next node on the queue
    # and check for the goal. If at the goal, copy the successful
    # path to the array of mazedata and then return 1. Else,
    # expand the node to the queue. 
    while q.size() > 0:       
        cur = q.dequeue() 
        if cur.traversed is False:
            #TODO: create search 
            cur.traversed = True
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
    short = 'A'
    if(dist[short] > dist['B']):
        short = 'B'
    if(dist[short] > dist['C']):
        short = 'C'
    if(dist[short] > dist['D']):
        short = 'D'
    if(dist[short] > dist['E']):
        short = 'E'
    return short