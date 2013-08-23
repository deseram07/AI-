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

# sample class
class Sample:
    def __init__(self, coordinates, cx, cy, x, y, angle):
        self.coords = coordinates
        self.cx = cx
        self.cy = cy
        self.x = x
        self.y = y
        self.angle = angle
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
        
# point class
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
# class for A* search
class Astar:
    def __init__(self):
        self.op = []
        heapq.heapify(self.op)
        self.cl = set()
        self.samples = []
        self.width = 1000
        self.grid = 50
        self.start = None
        self.end = None

# Returns the point reference of the asv and the transformed coordinates of
# the obstacles
def obstacle_transform(asv):
    index = 0
    ref_point = [asv[0].x, asv[0].y]
    obstacle_shift = [asv[0].y, asv[0].y, asv[0].x, asv[0].x]  # [-y, +y, -x, +x]
    
    for coordinate in asv:
        X = coordinate.x
        Y = coordinate.y
        
#        print X,Y
# expand obstacle to +x
        if X > ref_point[0] and X > obstacle_shift[2]:
            obstacle_shift[2] = X

# expand obstacle to left
        elif X < ref_point[0] and X < obstacle_shift[3]:
            obstacle_shift[3] = X

# expand obstacle to up
        if Y < ref_point[1] and Y < obstacle_shift[1]:
            obstacle_shift[1] = Y

# expand obstacle to down
        elif Y > ref_point[1] and Y > obstacle_shift[0]:
            obstacle_shift[0] = Y
            
# Calculate the required vectors additions that will be applied on
# obstacle coordinates
    for p in obstacle_shift:
        if index > 1:
            obstacle_shift[index] = ref_point[0] - obstacle_shift[index]
        else:
            obstacle_shift[index] = ref_point[1] - obstacle_shift[index]
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

# Return true if line segments AB and CD intersect
def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

def ccw(A, B, C):
    return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)

def centroid_angle(coords):
    num = len(coords) / 2
    sumx = 0
    sumy = 0
    for i in range(num):
        sumx = sumx + coords[i]
        sumy = sumy + coords[i + 1]
    cx = sumx / num
    cy = sumy / num
    angle = angles(Point(coords[0] + 1, coords[1]), Point(coords[0], coords[1]), Point(cx, cy))
    return cx, cy, angle
    
# Check for collisions returns True for a collision
def check_collision(obstacles, asv):
    pairs = [[0, 1, 2, 3], [2, 3, 4, 5], [4, 5, 6, 7], [6, 7, 0, 1]]
    for i in range(len(asv) - 1):
        for j in range(len(obstacles)):
            for k in range(len(pairs)):
                test = intersect(Point(asv[i].x, asv[i].y), Point(asv[i + 1].x, asv[i + 1].y), Point((obstacles[j])[(pairs[k])[0]], (obstacles[j])[(pairs[k])[1]]), Point((obstacles[j])[(pairs[k])[2]], (obstacles[j])[(pairs[k])[3]]))
                if test == True:
                    return True
    return False
