import sys
import numpy as np
import math

# creating an ASV
class ASV:
    def __init__(self, num, x, y):
        self.num = num
        self.x = x
        self.y = y
        self.previous = None
        self.boom = 0


# for printing the list of ASVs    
def print_asv(asv):
    for i in range(len(asv)):
        print str(asv[i].num) + ', ' + str(asv[i].x) + ', ' + str(asv[i].y) + ', ' + str(asv[i].previous)


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
