from gomoku import Gomoku

""" 
This module is the main module of part 2.2
"""

__author__ = 'Griffin A. Tucker / Michael Racine'
__version__ = '1.0'
__date__ = '2_19_18'

# only run the following code if we are at top level
if __name__ == "__main__":

    # get dimensions of Gomoku board and instantiate
    while True: 
        w = input("Please enter a value for the width of the Gomoku board: ")
        while:
            w = input("Invalid value: Please enter an integer: ")
        h = input("Please enter a value for the height of the Gomoku board: ")
        while:
            h = input("Invalid value: Please enter an integer: ")
        got_dimensions = input("Is " + str(w) + "x" + str(h) + " your desired dimensions? Enter 1 for yes; 0 for no: ")
        while got_dimensions != 0 and got_dimensions != 1:
            got_dimensions = input("Invalid input. Enter 1 for yes; 0 for no: ")
        if got_dimensions == 1: break;

    cur_board = Gomoku(w, h) 
