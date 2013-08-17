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
        self.destx = destx
        self.desty = desty
        self.boom = 0

# cell class
class CELL:
    def __init__(self, x, y, num, reachable):
        self.x = x
        self.y = y
        self.visited = num
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

# returns the estimated cost to destination from current position
def get_h(asv):
    dist = abs(asv.x - asv.destx) + abs(asv.y - asv.desty)
    return dist

