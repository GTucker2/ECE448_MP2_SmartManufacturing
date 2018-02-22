## author : Michael Racine 
## date: 2/21/18

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