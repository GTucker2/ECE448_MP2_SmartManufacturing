## author : Michael Racine 
## date: 3/6/18
#sys.setrecursionlimit(1500)
import Planning
import Widget
#creating distance dictionaries. They work like arrays but the index is the name of the 
#factory
start_dist  = {'A':0,    'B':0,   'C':0,   'D':0,   'E':0}
distances_A = {'A':0,    'B':1064,'C':673, 'D':1401,'E':277}
distances_B = {'A':1064, 'B':0,   'C':958, 'D':1934,'E':337}
distances_C = {'A':673,  'B':958, 'C':0,   'D':1001,'E':399}
distances_D = {'A':1401, 'B':1934,'C':1001,'D':0,   'E':387}
distances_E = {'A':277,  'B':337, 'C':399, 'D':387, 'E':0}


## Class that represents a tree filled with nodes created from a maze
class PlanTree:

    # initilize the nodes
    # param: self
    #        state: the state object corresponding to the node
    # return: initialized "MazeTree" hence refered to as a node
    def __init__(self, state):
        self.data = state
        self.A = None
        self.B = None
        self.C = None
        self.D = None
        self.E = None
        self.visited_from = "not"
        self.traversed = False 

# create the tree based on data
# param: self
# return: the root of the tree/graph
def create_tree():
    #initialize start state and widgets
    w1 = Widget.Widget('AEDCA')
    w2 = Widget.Widget('BEACD')
    w3 = Widget.Widget('BABCE')
    w4 = Widget.Widget('DADBD')
    w5 = Widget.Widget('BECBD')
    start_state = Planning.State('start', start_dist, {1:w1, 2:w2,3:w3, 4:w4,5:w5 })
    #create root
    root = PlanTree(start_state)
    #create children
    root.A = create_child(root.data.vars,distances_A,'A')
    root.B = create_child(root.data.vars,distances_B,'B')
    root.C = create_child(root.data.vars,distances_C,'C')
    root.D = create_child(root.data.vars,distances_D,'D')
    root.E = create_child(root.data.vars,distances_E,'E')
    # return the root
    return root
   
# create the tree based on data
# param: widgets: the wigdets that need to be completed
#        dists:   the distance dictionary the new state assosciates with
#        comp:    the component, a string, to add to the widgets and to label the state
# return: the relative root of the current tree/graph
def create_child(widgets,dists,comp):
    if widgets[1].done and widgets[2].done and widgets[3].done and widgets[4].done and widgets[5].done:
        return None
    new_state = Planning.State(comp, dists, {1:widgets[1].add_comp(comp), 2:widgets[2].add_comp(comp),
                                             3:widgets[3].add_comp(comp), 4:widgets[4].add_comp(comp),
                                             5:widgets[5].add_comp(comp) })
    curr_root = PlanTree(new_state)
    curr_root.A = create_child(curr_root.data.vars,distances_A,'A')
    curr_root.B = create_child(curr_root.data.vars,distances_B,'B')
    curr_root.C = create_child(curr_root.data.vars,distances_C,'C')
    curr_root.D = create_child(curr_root.data.vars,distances_D,'D')
    curr_root.E = create_child(curr_root.data.vars,distances_E,'E')
    return curr_root