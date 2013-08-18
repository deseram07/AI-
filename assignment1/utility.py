import sys
import numpy as np
import math
import heapq

# creating an ASV
class ASV:
    def __init__(self, num, x, y, destx, desty):
        self.num = num
        self.x = x
        self.y = y
        self.startx = x
        self.starty = y
        self.destx = destx
        self.desty = desty
        self.boom = 0

# cell class
class Cell:
    def __init__(self, x, y, reachable):
        self.x = x
        self.y = y
        self.visited = None
        self.reachable = reachable
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
        
# class for A* search
class Astar:
    def __init__(self):
        self.op = []
        heapq.heapify(self.op)
        self.cl = set()
        self.cells = []
        self.width = 1000
        self.height = 1000
        self.start = None
        self.end = None

# Returns the point reference of the asv and the transformed coordinates of
# the obstacles
def obstacle_transform(asv):
    index = 0
    ref_point = [asv[0].x, asv[0].y]
    obstacle_shift = [asv[0].y,asv[0].y,asv[0].x,asv[0].x]  #[up,down,left,right]
    
    for coordinate in asv:
        X = coordinate.x
        Y = coordinate.y
        
        print X,Y
# expand obstacle to right
        if X > ref_point[0] and X > obstacle_shift[3]:
            obstacle_shift[3] = X

# expand obstacle to left
        elif X < ref_point[0] and X < obstacle_shift[2]:
            obstacle_shift[2] = X

# expand obstacle to up
        if Y > ref_point[1] and Y > obstacle_shift[0]:
            obstacle_shift[0] = Y

# expand obstacle to down
        elif Y < ref_point[1] and Y < obstacle_shift[1]:
            obstacle_shift[1] = Y
            
# Calculate the required vectors additions that will be applied on
# obstacle coordinates
    for p in obstacle_shift:
        if index > 1:
            obstacle_shift[index] -= ref_point[0]
        else:
            obstacle_shift[index] -= ref_point[1]
        index += 1
    return obstacle_shift
            
            
# for printing the list of ASVs    
def print_asv(asv):
    for i in range(len(asv)):
        print str(asv[i].num) + ', ' + str(asv[i].x) + ', ' + str(asv[i].y)

# takes a list of string decimals and converts to a number and returns list of ints
def remove_decimal(list):
    for i in range(len(list)):
        list[i] = int(float(list[i]) * 1000)
        
    return list

# calculates the distance between two points
def boom_length(start, end):
    boom = math.sqrt((start.x - end.x) ** 2 + (start.y - end.y) ** 2)
    return boom

# calculates angle between 3 ASVs
def angles(start, middle, end):
    a = boom_length(middle, end)
    b = boom_length(start, middle)
    c = boom_length(start, end)
    angle = math.degrees(math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b)))
    return angle

    
