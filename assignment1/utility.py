import sys
import numpy as np
import math
import heapq
import random
import time
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

# sample class
class Sample:
    def __init__(self, coordinates, cx, cy, x, y):#, angle):
        self.coords = coordinates
        self.cx = cx
        self.cy = cy
        self.x = x
        self.y = y
#         self.angle = angle
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
        self.grid = 10
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
        
    add = add + (asv[number - 1].x * asv[0].y - asv[number - 1].y * asv[0].x)
    return abs(add / 2)

# Return true if line segments AB and CD intersect
def intersect(A, B, C, D):
    return np.sign(ccw(A, C, D)) != np.sign(ccw(B, C, D)) and np.sign(ccw(A, B, C)) != np.sign(ccw(A, B, D))
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
    
    n = len(asv)  # number of asv's
#    obtaining random lengths for booms
    for i in range(len(asv) - 1):
        lengths.append(random.randrange(50, 75))
    
#    obtaining random angles between booms
    for i in range(n - 1):
        angle_sample.append(random.random())
    angle_sample.append(1.0)
    angle_sample.sort()

    for i in range(len(angle_sample) - 1):
        pre_angles.append((angle_sample[i + 1] - angle_sample[i]) * 2.0 * np.pi)
   
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

def generate_coordinates(lengths, angles, asv, grid, obstacles):
    init_coord = [0, 0]
    coordinate = []
#    placing the point in random location, this ensures that point lies on gird
    shift = [(random.random()) * 1000.0, (random.random()) * 1000.0]
    rotate = random.random() * np.pi * 2.0
    
#    first find the points with initial boom on x axis with 0 degree rotation
    coordinate.append(init_coord)
    coordinate.append([init_coord[0] + lengths.pop(0), init_coord[1]])
    for i in range(len(lengths)):
        [x, y] = coordinate[-1]
        angle = angles.pop(0)
        length = lengths.pop(0)
        x = x + (length * np.cos(angle))
        y = y + (length * np.sin(angle))
        coordinate.append([x, y])
    
    if check1(coordinate, asv):
        shift = Shift(coordinate, shift)
        coordinate = Rotate2D(shift, rotate)
        return check2(coordinate, asv, grid, obstacles)
#         return True
    else:
        return False
    
    
def check2(coordinate, asv, grid, obstacles):
    for coord, ASV in zip(coordinate, asv):
        ASV.x = coord[0]
        ASV.y = coord[1]
    
    # boom in obstacle (True for collision)
    if check_collision(obstacles, asv) == False:
        for i in asv:
            if 0 <= i.x <= 1000 and  0 <= i.y <= 1000:
                # coord not in obstacle
                if grid[i.y][i.x] == 0:
                    pass
            else:
                return False
        return True
    return False

def check1(coordinate, asv):
    for coord, ASV in zip(coordinate, asv):
        ASV.x = coord[0]
        ASV.y = coord[1]
    A = area(asv)
    n = len(asv)
    r_min = 7 * (n - 1)
    min_area = np.pi * r_min ** 2  # minimum allowed area
    
    """
    Area greater than min_area
    All points within (1000,1000) grid
    ASV combination not in obstacle
    """
    # greater area
    if A > min_area:
        for i in range(len(asv) - 1):
            if np.sign(ccw(asv[i - 1], asv[i], asv[i + 1])) != np.sign(asv[0].direction):
                return False
        if np.sign(ccw(asv[-2], asv[-1], asv[0])) != np.sign(asv[0].direction):
            return False
        return True
    
    return False


def Shift(pts, delta):
    [dx, dy] = delta
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
    cnt = np.array([0, 0])
    return (np.dot(pts - cnt, np.array([[np.cos(ang), np.sin(ang)], [-np.sin(ang), np.cos(ang)]])) + cnt).tolist()
    
def obtain_random_points(asv, n=5, obstacles=[-1, -1, -1, -1],grid=np.zeros(shape=(1000, 1000))):
    points = []
    sample = []
    x = []
    y = []
    count = 0
    while count < n:
        lengths, angles = random_length_angle(asv)
        if generate_coordinates(lengths, angles, asv, grid, obstacles):
            for i in asv:
                sample.append(int(i.x))
                sample.append(int(i.y))
                x.append(int(i.x))
                y.append(int(i.y))
            points.append(sample)
            if debug:
                ox1 = [0,200,200,0,0]
                ox2 = [500,700,700,500,500]
                oy1 = [200,200,400,400,200]
                oy2 = [600,600,900,900, 600]
                py.plot(ox1, oy1, '-+')
                py.plot(ox2, oy2, '-+')
                py.plot(x, y, '-+')
                py.show()
                x = []
                y = []
            sample = []
            count += 1
    return points

def constrained_sum_sample_pos(n, total):
    """Return a randomly chosen list of n positive integers summing to total.
    Each such list is equally likely to occur."""

    dividers = sorted(random.sample(xrange(1, total), n - 1))
    return [a - b for a, b in zip(dividers + [total], [0] + dividers)]
    
# Check for collisions returns True for a collision
def check_collision(obstacles, asv):
    pairs = [[0, 1, 2, 3], [2, 3, 4, 5], [4, 5, 6, 7], [6, 7, 0, 1]]
    for i in range(len(asv) - 1):
        for j in range(len(obstacles)):
            for k in range(len(pairs)):
                if intersect(Point(asv[i].x, asv[i].y), Point(asv[i + 1].x, asv[i + 1].y), Point((obstacles[j])[(pairs[k])[0]], (obstacles[j])[(pairs[k])[1]]), Point((obstacles[j])[(pairs[k])[2]], (obstacles[j])[(pairs[k])[3]])):
                    return True
    return False

def centroid_angle(coords):
    num = len(coords) / 2
    sumx = 0
    sumy = 0
#     print coords
    for i in range(num):
        sumx = sumx + coords[i]
        sumy = sumy + coords[i+1]
    cx = sumx / num
    cy = sumy / num
#     angle = angles(Point(coords[0] + 1, coords[1]), Point(coords[0], coords[1]), Point(cx, cy))
    return cx, cy #, angle

def interpolate(current, previous):
#    assuming that the coordinates provided at x0,y0,x1,y1,x2,y2
    moves = []
    move = []
    x = True
    print current,previous
    while True:
        if current == previous:
            break
        for index in range(len(current)/2):
            if x:
                i =index * 2
            else:
                i =(index * 2) + 1
            if round(current[i],3) != round(previous[i],3):
                previous[i] = round(previous[i] + (np.sign(current[i] - previous[i]) * 0.001),3)
        if x:
            x = False
        else:
            x = True
#        print previous
        for i in previous:
            move.append(i)
        moves.append(move)
        move = []
    return moves
            
        
        
        
