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
    prev = None
    while not q.empty():       
        cur = q.get() 
        if prev == cur:
            prev = cur
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
            if next not in curr_cost or update_cost < curr_cost[next]:
                curr_cost[next] = update_cost
            prior = curr_cost[next] + stop_hist(end,next,5)
            q.put(next, prior)       
        prev = cur
        
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
    prev = None
    while not q.empty():       
        cur = q.get() 
        if prev == cur:
            prev = cur
            cur = q.get()
        nodes_expanded = nodes_expanded + 1
        end[1].add_comp(cur)
        end[2].add_comp(cur)
        end[3].add_comp(cur)
        end[4].add_comp(cur)
        end[5].add_comp(cur)
        if prev is not None and prev != cur:
            miles_traveled = miles_traveled + graph.cost(prev, cur)
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
            prior = update_cost + dist_hist(graph.weights[cur],end,next,5)
            q.put(next, prior)           
        prev = cur
    # Return the failed because solution was not found
    solution = 'FAILED'
    miles_traveled = -1
    return (solution, miles_traveled, nodes_expanded)

#histogram to find the most common component
#param:  comps    : list of the next components to check
#        n        : possible number of components
#        next_comp: the compenent to calculate the cost
#return: number of times character appears in widgets
def stop_hist(comps,next_comp, n):
    count = 0
    total_num = (n*5)
    for i in range(1,n):
        if comps[i].done == False:
            total_num = total_num - (len(comps[i].needed) - len(comps[i].current_string))
            temp = comps[i].needed.partition(comps[i].next_char)
            temp_str = temp[1] + temp[2]
            if comps[i].next_char == next_comp:
                count = count + temp_str.count(next_comp) - 1
            else:
                count = count + temp_str.count(next_comp) 
        else:
            total_num = total_num - len(comps[i].needed)
    num_appear = abs(total_num - count)
    return num_appear

#histogram to find the shortest distance to a widget
#param:  dist     : list of distances to other components
#        n        : possible number of components
#        next_comp: the compenent to calculate the cost
#        comps    : list of the next components to check
#return: number of times character appears in widgets time the distance between nodes
def dist_hist(dist, comps, next_comp, n):
    count = stop_hist(comps, next_comp, n)
    return dist[next_comp] * count

#finds the path with the least number of stops
#param:  start: starting  state for the search
#return: string of path taken
def dijkstra_smallest_stops(graph, start, end):
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
            prior = curr_cost[next]
            q.put(next, prior)          
        
    # Return the failed because solution was not found
    solution = 'FAILED: ' + solution
    return (solution, nodes_expanded)

#finds the path with the least number of stops
#param:  start: starting  state for the search
#return: string of path taken
def dijkstra_shortest_dist(graph, start, end):
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
            prior = update_cost
            q.put(next, prior)           
            miles_traveled = miles_traveled + graph.cost(cur, next)
    # Return the failed because solution was not found
    solution = 'FAILED'
    miles_traveled = -1
    return (solution, miles_traveled, nodes_expanded)