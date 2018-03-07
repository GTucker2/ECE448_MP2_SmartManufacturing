## author : Michael Racine 
## date: 3/7/18


#Graph class based on code from https://www.redblobgames.com/pathfinding/a-star/implementation.html
class Graph:
    def __init__(self):
        self.edges = {}
        self.weights = {}
    
    def neighbors(self, id):
        return self.edges[id]

    def cost(self, fnode, tnode):
        return self.weights.get(fnode, 1)[tnode]



