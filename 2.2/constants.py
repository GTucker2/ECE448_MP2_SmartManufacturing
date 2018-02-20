""" This module defines a set of constants to
be used with the 2.2 project. All constants are
private and must be accessed as if they were 
functions, e.g. constants.DATA
"""
__author__ = 'Griffin A. Tucker'
__version__ = '1.0'
__date__ = '2_19_18'

# The minimum possible height and width of the 
# Gomoku board. 
__HEIGHT_MIN = 0
__WIDTH_MIN = 0
__DEFAULT_HEIGHT = 7
__DEFAULT_WIDTH = 7

# The types of things which a Gomoku board tile may contain
__RED_TILE = 1
__BLUE_TILE = -1
__BLANK_TILE = 0
__TILE_TYPES = [__RED_TILE, __BLUE_TILE, __BLANK_TILE]

# Getter functions for the aforementioned constants
def HEIGHT_MIN(): return __HEIGHT_MIN
def WIDTH_MIN(): return __WIDTH_MIN
def DEFAULT_HEIGHT(): return __DEFAULT_HEIGHT
def DEFAULT_WIDTH(): return __DEFAULT_WIDTH
def TILE_TYPES(): return __TILE_TYPES
def RED_TILE(): return __TILE_TYPES[0]
def BLUE_TILE(): return __TILE_TYPES[1]
def BLANK_TILE(): return __TILE_TYPES[2]