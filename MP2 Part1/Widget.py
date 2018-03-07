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

    # add a component to the widget
    # param: self
    #        comp: the character component to add to the widget
    # return: None
    def add_comp(self, comp):
        #widget already finished return so it isn't modified
        if self.done:
            return
        #if the widget isn't done and the component is the next needed component then concatenate
        if self.next_char == comp and self.next_idx < len(self.needed):
            self.current_string = self.current_string+comp
            if self.next_idx == len(self.needed)-1:
                self.next_char = 'DONE'
                self.next_idx = -1
            else:
                self.next_char = self.needed[self.next_idx+1]
                self.next_idx = self.next_idx+1
        else: return

        if self.current_string == self.needed:
            self.done = True




