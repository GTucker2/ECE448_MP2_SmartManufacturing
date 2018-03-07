import Planning
import Widget
import PlanTree
import graph

#part 1 Q1
w1 = Widget.Widget('AEDCA')
w2 = Widget.Widget('BEACD')
w3 = Widget.Widget('BABCE')
w4 = Widget.Widget('DADBD')
w5 = Widget.Widget('BECBD')
short_graph = graph.Graph()
short_graph.edges = {
    'start' : ['A','B','C','D','E'],
    'A': ['A','B','C','D','E'],
    'B': ['A','B','C','D','E'],
    'C': ['A','B','C','D','E'],
    'D': ['A','B','C','D','E'],
    'E': ['A','B','C','D','E']
    }
short_graph.weights ={
    'start' : {'A':0,    'B':0,   'C':0,   'D':0,   'E':0},
    'A' : {'A':0,    'B':1064,'C':673, 'D':1401,'E':277},
    'B' : {'A':1064, 'B':0,   'C':958, 'D':1934,'E':337},
    'C' : {'A':673,  'B':958, 'C':0,   'D':1001,'E':399},
    'D' : {'A':1401, 'B':1934,'C':1001,'D':0,   'E':387},
    'E' : {'A':277,  'B':337, 'C':399, 'D':387, 'E':0}   
    }
shortest_path = Planning.search_shortest_dist(short_graph, 'start', {1:w1, 2:w2,3:w3, 4:w4,5:w5})
#part 1 Q2
dist_graph = graph.Graph()
dist_graph.edges = {
    'start' : ['A','B','C','D','E'],
    'A': ['A','B','C','D','E'],
    'B': ['A','B','C','D','E'],
    'C': ['A','B','C','D','E'],
    'D': ['A','B','C','D','E'],
    'E': ['A','B','C','D','E']
    }
dist_graph.weights ={
    'start' : {'A':0,    'B':0,   'C':0,   'D':0,   'E':0},
    'A' : {'A':0,    'B':1064,'C':673, 'D':1401,'E':277},
    'B' : {'A':1064, 'B':0,   'C':958, 'D':1934,'E':337},
    'C' : {'A':673,  'B':958, 'C':0,   'D':1001,'E':399},
    'D' : {'A':1401, 'B':1934,'C':1001,'D':0,   'E':387},
    'E' : {'A':277,  'B':337, 'C':399, 'D':387, 'E':0}   
    }
shortest_dist = Planning.search_shortest_dist(dist_graph, 'start', {1:w1, 2:w2,3:w3, 4:w4,5:w5})


