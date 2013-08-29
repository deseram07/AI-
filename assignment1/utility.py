import sys
import numpy as np
import math
import heapq
import random
import pylab as py
debug = 0
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
        self.direction = None

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

# calculate area of asv shape
def area(asv):
    add = 0
    number = len(asv)
    for i in range(number - 1):
        add = add + (asv[i].x * asv[i + 1].y - asv[i].y * asv[i + 1].x)
        
    add = add + (asv[number-1].x * asv[0].y - asv[number-1].y * asv[0].x)
    return abs(add / 2)

# Return true if line segments AB and CD intersect
def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
def ccw(A, B, C):
#    True if direction is counter clockwise
    return (C.y - A.y) * (B.x - A.x) - (B.y - A.y) * (C.x - A.x)

# Selects random lengths for asv booms and random angles between asvs
# and returns if the area is greater than 
def random_length_angle(asv):
    angles = []
    pre_angles = []
    angle_sample = [0.0]
    lengths = []
    
    n = len(asv)    #number of asv's
#    obtaining random lengths for booms
    for i in range(len(asv)-1):
        lengths.append(random.randrange(50,75))
    
#    obtaining random angles between booms
    for i in range(n-1):
        angle_sample.append(random.random())
    angle_sample.append(1.0)
    angle_sample.sort()

    for i in range(len(angle_sample)-1):
        pre_angles.append((angle_sample[i+1] - angle_sample[i])*2.0*np.pi)
   
    if asv[0].direction < 0:
#        if rotating clockwise
        i = 0
        for i in range(len(pre_angles)):
            angle = pre_angles[i]
            for j in pre_angles[:i]:
                angle += j
            angles.append(-angle)
    else:
#        if rotating counterclockwise
        i = 0
        for i in range(len(pre_angles)):
            angle = pre_angles[i]
            for j in pre_angles[:i]:
                angle += j
            angles.append(angle)
    return lengths, angles

def generate_coordinates(lengths, angles, asv):
    init_coord = [0,0]
    coordinate = []
#    placing the point in random location, this ensures that point lies on gird
    shift = [(random.random())*1000.0,(random.random())*1000.0]
    rotate = random.random() * np.pi * 2.0
    
#    first find the points with initial boom on x axis with 0 degree rotation
    coordinate.append(init_coord)
    coordinate.append([init_coord[0]+ lengths.pop(0),init_coord[1]])
    for i in range(len(lengths)):
        [x,y] = coordinate[-1]
        angle = angles.pop(0)
        length = lengths.pop(0)
        x = x + (length * np.cos(angle))
        y = y + (length * np.sin(angle))
        coordinate.append([x,y])
    
    if check(coordinate,asv):
        shift = Shift(coordinate,shift)
        coordinate = Rotate2D(shift, rotate)
        return True
    else:
        return False
    

def check(coordinate,asv):
    for coord,ASV in zip(coordinate, asv):
        ASV.x = coord[0]
        ASV.y = coord[1]
    A = area(asv)
    n = len(asv)
    r_min = 7*(n-1)
    min_area = np.pi * r_min**2 # minimum allowed area
    
    """
    Area greater than min_area
    All points within (1000,1000) grid
    ASV combination not in obstacle
    """
    for i in asv:
        if 0 <= i.x <= 1000 and  0 <= i.y <= 1000:
            pass
        else:
            return False
    for i in range(len(asv)-1):
        if np.sign(ccw(asv[i-1],asv[i],asv[i+1])) != np.sign(asv[0].direction):
            return False
    if np.sign(ccw(asv[-2],asv[-1],asv[0])) != np.sign(asv[0].direction):
        return False 
    return A>min_area


def Shift(pts, delta):
    [dx,dy] = delta
    for i in range(len(pts)):
        pts[i][0] += dx
        pts[i][1] += dy
    return pts

def Rotate2D(pts, ang):
    """
    Rotates a gives polygon about the origin in the counter clockwise direction 
    by (thetha) degrees
    """
    pts = np.array(pts)
    cnt = np.array([0,0])
    return (np.dot(pts-cnt,np.array([[np.cos(ang),np.sin(ang)],[-np.sin(ang),np.cos(ang)]]))+cnt).tolist()
    
def obtain_random_points(asv, n = 5):
    points = []
    sample = []
    x = []
    y = []
    count = 0
    while count < n:
        lengths, angles = random_length_angle(asv)
        if generate_coordinates(lengths, angles, asv):
            for i in asv:
                sample.append([int(i.x),int(i.y)])
                x.append(int(i.x))
                y.append(int(i.y))
            points.append(sample)
            if debug:
                py.plot(x,y, '-+')
                py.show()
                x= []
                y = []
            sample = []
            count += 1
    return points

def constrained_sum_sample_pos(n, total):
    """Return a randomly chosen list of n positive integers summing to total.
    Each such list is equally likely to occur."""

    dividers = sorted(random.sample(xrange(1, total), n - 1))
    return [a - b for a, b in zip(dividers + [total], [0] + dividers)]
    
    
