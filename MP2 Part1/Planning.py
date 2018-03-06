## author : Michael Racine 
## date: 2/21/18

import queue

#creating distance dictionaries, don't need these yet so they are commented out. They work like arrays but the index is the name of the 
#factory
#start_dist  = {'A':0,    'B':0,   'C':0,   'D':0,   'E':0}
#distances_A = {'A':0,    'B':1064,'C':673, 'D':1401,'E':277}
#distances_B = {'A':1064, 'B':0,   'C':958, 'D':1934,'E':337}
#distances_C = {'A':673,  'B':958, 'C':0,   'D':1001,'E':399}
#distances_D = {'A':1401, 'B':1934,'C':1001,'D':0,   'E':387}
#distances_E = {'A':277,  'B':337, 'C':399, 'D':387, 'E':0}
#string to hold the solution of the search
solution = ''

#class that creates the states to go between. 
class State:
    #creates a State object
    #param:  self
    #        name: the name of the state as a string
    #        dists: distance to the other states as an array of ints
    #return: State object
    def __init__(self, name, dists):
        self.loc = name
        self.distance_to = dists

    #finds the path with the least number of stops
    #param:  start-starting  state for the search
    #return: string of path taken
    def search_smallest_stops(start):
        ret_val = []


        return

    #finds the path with the least number of stops
    #param:  start-starting  state for the search
    #return: string of path taken
    def search_shortest_dist(start):
        ret_val = []
        return

    #histogram to find the most common component
    #param:  comps-list of the next components to check
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
    #param:  dist-list of distances to other components
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