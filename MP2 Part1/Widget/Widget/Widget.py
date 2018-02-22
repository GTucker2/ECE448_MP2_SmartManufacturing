## author : Michael Racine 
## date: 2/21/18

#class that represents the widgets to be created
class Widget:

    # initilize the nodes
    # param: self
    #        param: the string representing the whole widget
    # return: Widget class object
    def __init__(self, param):
        self.needed = param
        self.current_string = ''
        self.next_char = param[0]
        self.next_idx = 0
        self.done = False



