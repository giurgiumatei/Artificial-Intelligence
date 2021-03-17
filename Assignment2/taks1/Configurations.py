

# import the pygame module, so you can use it
import pickle,pygame,time
from math import sqrt

from pygame.locals import *
from random import random, randint
import numpy as np


#Creating some colors
BLUE  = (0, 0, 255)
GRAYBLUE = (50,120,120)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

#define indexes variations
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]

def manhattan_function_h(x2, x1, y2, y1): #cost heuristic function from the current state to the final state
    return abs(x2 - x1) + abs(y2 - y1)

def manhattan_function_g(x1, x3, y1, y3): #cost function from the initial state to the current state
    return abs(x1 - x3) + abs(y1 - y3)

def manhattan_function_f(x2, x1, y2, y1, x3, y3): #cost estimation of the path
    result = manhattan_function_h(x2, x1, y2, y1) + manhattan_function_g(x1, x3, y1, y3)
    return result


def function_h(x2, x1, y2, y1): #cost heuristic function from the current state to the final state
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

def function_g(x1, x3, y1, y3): #cost function from the initial state to the current state
    return sqrt((x1 - x3)**2 + (y1 - y3)**2)

# def function_f(x2, x1, y2, y1, x3, y3, cost_so_far): #cost estimation of the path
#     result = function_h(x2, x1, y2, y1) + function_g(x1, x3, y1, y3) + cost_so_far[(x1, y1)]
#     return result
def function_f(x2, x1, y2, y1, x3, y3, cost_so_far): #cost estimation of the path
    result = function_h(x2, x1, y2, y1) + function_g(x1, x3, y1, y3) + cost_so_far[(x1, y1)]
    return result
