import sys
import numpy as np
import math
import heapq
import random
import copy
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
    def __init__(self, coordinates):
        self.coords = coordinates
        self.points = []
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
        self.obstacle_x = []
        self.obstacle_y = []
        heapq.heapify(self.op)
        self.cl = set()
        self.samples = []
        self.width = 1000
        self.grid = 100
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
    angle = (math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b)))
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

def check_coordinates(lengths, angles, asv, AStar, rotate, shift):
    init_coord = [0, 0]
    coordinate = []
    xxx = []
    yyy = []
    
#    first find the points with initial boom on x axis with 0 degree rotation
    coordinate.append(init_coord)
    coordinate.append([init_coord[0] + lengths[0], init_coord[1]])
    for i in range(1,len(lengths)):
        [x, y] = coordinate[-1]
        angle = angles[i-1]
        length = lengths[i]
        x = x + (length * np.cos(angle))
        y = y + (length * np.sin(angle))
        coordinate.append([x, y])
    
    if check1(coordinate, asv):
        
        shift = Shift(coordinate, shift)
        coordinate = Rotate2D(shift, rotate, shift[0])
#         print coordinate
        return check2(coordinate, asv, AStar)
#         return True
    else:
        return False
    
def obtain_coordinates(point,AStar):
    [shift_x,shift_y,rotate,lengths,angles] = point
    init_coord = [0,0]
    xxx = []
    yyy = []
    shift = [shift_x,shift_y]
    coordinate = []
    
    coordinate.append(init_coord)
    coordinate.append([init_coord[0] + lengths[0], init_coord[1]])
    for i in range(1,len(lengths)):
        [x, y] = coordinate[-1]
        angle = angles[i-1]
        length = lengths[i]
        x = x + (length * np.cos(angle))
        y = y + (length * np.sin(angle))
        coordinate.append([x, y])
    
#    for i in coordinate:
#        xxx.append(i[0])
#        yyy.append(i[1])
#    py.plot(xxx,yyy,'+-')
#    py.show()
#    xxx = []
#    yyy = []
    
    shift = Shift(coordinate, shift)
#    for i in shift:
#        xxx.append(i[0])
#        yyy.append(i[1])
#    py.plot(xxx,yyy,'+-')
#    py.show()
#    xxx = []
#    yyy = []

    coordinate = Rotate2D(shift, rotate, shift[0])
#    for i in coordinate:
#        xxx.append(i[0])
#        yyy.append(i[1])
#    py.plot(xxx,yyy,'+-')
#    py.show()
    return dup_check2(coordinate, AStar)
        
def check2(coordinate, asv, AStar):
    for coord, ASV in zip(coordinate, asv):
        ASV.x = coord[0]
        ASV.y = coord[1]
    
    obstacle_x = AStar.obstacle_x
    obstacle_y = AStar.obstacle_y

    if check_collision(AStar, asv) == False:
        for i in asv:
            if 0 <= i.x <= 1000 and  0 <= i.y <= 1000:
                # coord not in obstacle
                for o in range(len(obstacle_x)):
                    if obstacle_x[o][0] <= i.x and obstacle_x[o][1] >= i.x and obstacle_y[o][0] <= i.y and obstacle_y[o][1] >= i.y:
                        return False
            else:
                return False
        return True
    return False

def dup_check2(coordinate, AStar):

    
    obstacle_x = AStar.obstacle_x
    obstacle_y = AStar.obstacle_y
#    print coordinate
    if debug:
        print "obstacle_x = ", obstacle_x
        print "obstacle_y = ", obstacle_y
        print "Coordinate checked = ", coordinate
          
    # boom in obstacle (True for collision)
    if dup_check_collision(AStar,coordinate) == False:  ##!!!!! need to make a function without the asv but coordinate
        for i in range(len(coordinate)):
            if 0 <= coordinate[i][0] <= 1000 and  0 <= coordinate[i][1] <= 1000:
                # coord not in obstacle
                for o in range(len(obstacle_x)):
                    if obstacle_x[o][0] <= coordinate[i][0] and obstacle_x[o][1] >= coordinate[i][0] and obstacle_y[o][0] <= coordinate[i][1] and obstacle_y[o][1] >= coordinate[i][1]:
                        return -1
            else:
                return -1
        return coordinate
    return -1

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

def Rotate2D(pts, ang, midpoint = [0, 0]):
    """
    Rotates a gives polygon about the origin in the counter clockwise direction 
    by (thetha) degrees
    """
    pts = np.array(pts)
    cnt = np.array(midpoint)
    return (np.dot(pts - cnt, np.array([[np.cos(ang), np.sin(ang)], [-np.sin(ang), np.cos(ang)]])) + cnt).tolist()
    
def obtain_random_points(asv, AStar, n=5):
    points = []
    sample = []
    x = []
    y = []
    count = 0

    while count < n:
        #    placing the point in random location, this ensures that point lies on gird
        shift = [(random.random()) * 1000.0, (random.random()) * 1000.0]
        rotate = random.random() * np.pi * 2.0
        lengths, angles = random_length_angle(asv)
        
        if check_coordinates(lengths, angles, asv, AStar, rotate, shift):
            for i in shift:
                sample.append(i)
            sample.append(rotate)
            sample.append(lengths)
            sample.append(angles[:-2])

            points.append(sample)
            if debug:
                for i in range(len(oxs)):
                    py.plot(oxs[i], oys[i], '-+')
                py.plot(x, y, '-+')
                py.show()
                x = []
                y = []
            sample = []
            count += 1
    print "Finished sampling"
    return points

def constrained_sum_sample_pos(n, total):
    """Return a randomly chosen list of n positive integers summing to total.
    Each such list is equally likely to occur."""

    dividers = sorted(random.sample(xrange(1, total), n - 1))
    return [a - b for a, b in zip(dividers + [total], [0] + dividers)]

def dup_check_collision(AStar, coordinates):
    corners = []
    for k in AStar.obstacle_x:
        for l in AStar.obstacle_y:
            minx = k[0]
            miny = l[0]
            maxx = k[1]
            maxy = l[1]
            corners.append([Point(minx,miny), Point(minx,maxy), Point(maxx,miny), Point(maxx,maxy)])
        
    for i in range(len(coordinates)/2 - 1):
        for k in corners:
            for l in range(len(k)-1):
                A = Point(coordinates[i*2], coordinates[i*2+1])
                B = Point(coordinates[(i + 1)*2], coordinates[(i + 1)*2+1])
                C = k[l]
                if l == len(k):
                    D = k[0]
                else:
                    D = k[l+1]
                if intersect(A, B, C, D):
                    return True
    return False

# Check for collisions returns True for a collision
def check_collision(AStar, asv):
    corners = []
    for k in AStar.obstacle_x:
        for l in AStar.obstacle_y:
            minx = k[0]
            miny = l[0]
            maxx = k[1]
            maxy = l[1]
            corners.append([Point(minx,miny), Point(minx,maxy), Point(maxx,miny), Point(maxx,maxy)])
            
    for i in range(len(asv) - 1):
        for j in AStar.obstacle_x:
            for k in corners:
                for l in range(len(k)-1):
                    A = Point(asv[i].x, asv[i].y)
                    B = Point(asv[i + 1].x, asv[i + 1].y)
                    C = k[l]
                    if l == len(k):
                        D = k[0]
                    else:
                        D = k[l+1]
                    if intersect(A, B, C, D):
                        return True
    return False

def interpolate2(cur, prev):
    current = cur[:]
    previous = prev[:]
    moves = []
    move = None
    
    while current != previous:
        for i in range(len(current)):
            if round(previous[i],3) != round(current[i],3):
                previous[i] = round(previous[i] + (np.sign(current[i] - previous[i])) * 0.001,3)
        print previous
        move = previous[:]
        moves.append(move)
    return moves 

def interpolate(cur, prev):
    current = cur[:]
    previous = prev[:]
    
#    assuming that the coordinates provided at x0,y0,x1,y1,x2,y2
    for i in range(len(current)):
        current[i] = round(current[i],3)
        previous[i] = round(previous[i],3)
    moves = []
    move = []
    x = True
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
        for i in previous:
            move.append(i)
        moves.append(move)
        move = []
    return moves

def extract_points(new, origin, AStar,cSpace):
    
    steps = []
    index = 0
    route = interpolate([new[0]/1000.0,new[1]/1000.0],[origin[0]/1000.0,origin[1]/1000.0])
    
    for point in route:
        for o in range(len(AStar.obstacle_x)):
            if AStar.obstacle_x[o][0] <= point[0] and AStar.obstacle_x[o][1] >= point[0] and AStar.obstacle_y[o][0] <= point[1] and AStar.obstacle_y[o][1] >= point[1]:
                return [None,-1]

    No_step = len(route)
    if not No_step:
        No_step = 1 
        route.append([new[0],new[1]])
    delta_gamma = (new[2] - origin[2])/No_step
    delta_angles = []
    
    for i in range(len(new[4])):
        delta_angles.append((new[4][i] - origin[4][i])/float(No_step))

    prev_config = origin[:]
    
    steps.append(obtain_coordinates(prev_config,AStar))

    if steps[-1] == -1:
        return [None,-1]
    
    for index in range(No_step):
        prev_config[0] = route[index][0]*1000.0
        prev_config[1] = route[index][1]*1000.0
        prev_config[2] = prev_config[2] + delta_gamma
        for i in range(len(prev_config[4])):
            prev_config[4][i] = prev_config[4][i] + delta_angles[i]
        steps.append(obtain_coordinates(prev_config,AStar))
        if steps[-1] == -1:
            return [None,-1]
    return [steps,No_step]
        
