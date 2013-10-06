import numpy as np
import math
from vectors import *

class Tracker:
    def __init__(self, m, num, policy, goal, targetParam, targetState, params, state, obstacles, C):
        self.m = m  # grid size, ie number of rows or number of columns
        self.num = num  # number of targets
        self.policy = policy  # array[m][m] = 0->8 actions
        self.goal = goal  # finish area [[minx, miny], [maxx, maxy]]
        self.targetParam = targetParam  # [alpha, ra]
        self.targetMotion = None  # probability map array[action][outcome]
        self.targetState = targetState  # [x, y, theta]
        self.motionHist = None  # probability map array[action][outcome]
        self.params = params  # [(minLength, maxLength,) beta, rb]
        self.state = state  # [x, y, theta (, length)]
        self.obstacles = obstacles  # [[[minx, miny], [maxx, maxy]],[....]]
        self.desiredAction = None 
        self.C = C  # int 0 for using eyes, 1 for using camera on stick
        self.statespace = [[-1,1],[-0.5,1],[0,1],[0.5,1],[1,1],[-1,0.5],[-0.5,0.5],[0,0.5],[0.5,0.5],[1,0.5],
                            [-1,0],[-0.5,0],[0,0],[0.5,0],[1,0],[-1,-0.5],[-0.5,-0.5],[0,-0.5],[0.5,-0.5],[1,-0.5],
                            [-1,-1],[-0.5,-1],[0,-1],[-0.5,-0.5],[-1,-1]]
        self.actionspace = [1,2,3,5,6,8,9,10,12,14,15,16,18,19,21,22,23]
        
class Target:
    def __init__(self, m, num, policy, goal, targetParam, targetState, obstacles, A):
        self.m = m  # grid size, ie number of rows or number of columns
        self.num = num  # number of targets
        self.policy = policy  # array[m][m] = 0->8 actions
        self.goal = goal  # finish area [[minx, miny], [maxx, maxy]]
        self.params = targetParam  # [alpha, ra]
        self.motionHist = None  # probability map array[action][outcome]
        self.state = targetState  # [x, y, theta]
        self.obstacles = obstacles  # [[[minx, miny], [maxx, maxy]],[....]]
        self.A = A  # movement type, 0 completely random, 1 modeled random
        self.actionspace = [[-1,1],[0,1],[1,1],[-1,0],[0,0],[1,0],[-1,-1],[0,-1],[1,-1]]

        
def target_motion_history(file_1):
    data = open(file_1, 'r')
    lines = data.readlines()
    init = float(lines.pop(0).strip('\r\n'))
    prob_map = np.zeros(shape=(9, 9))
    count = 0.0
    for line in lines:
        list = line.strip('\n').strip('\r').split(' ')
        prob_map[int(list[0])][int(list[1])] += 1
        
    for i in range(9):
        sum = 0
        for j in range(9):
            sum += prob_map[i][j]
        for j in range(9):
            prob_map[i][j] /= sum
    data.close()
    return prob_map
        
# function used to determine the divergence probability from previous data Stohcastic model
def tracker_motion_history(file_1):
    data = open(file_1, 'r')
    lines = data.readlines()
    init = float(lines.pop(0).strip('\r\n'))
    prob_map = np.zeros(shape=(25, 25))
    for line in lines:
        list = line.strip('\n').strip('\r').split(' ')
        prob_map[int(list[0])][int(list[1])] += 1
    
    for i in range(25):
        sum = 0
        for j in range(25):
            sum += prob_map[i][j]
        if sum != 0:
            for j in range(25):
                prob_map[i][j] /= sum
    data.close()
    return prob_map

# Checks if target inside finish area
def finish(goal, target_pos):
    return point_in_polygon(goal, target_pos)

# check in coordinate is inside polygon (works for state inside polygon)
def point_in_polygon(polygon, point):
    # polygon = [[minX, minY], [maxX, maxY]], point = [x, y]
    if point[0] >= polygon[0][0] and point[0] <= polygon[1][0] and polygon[0][1] <= point[1] and point[1] <= polygon[1][1]:
        return True
    return False

# Function used to determine which cells can be observed by the tracker at its state
def observation(tracker):
    cells = []
    
    return cells

# distance between two points
def dist(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

# calculates angle between 3 ASVs
def angle(start, middle, end):
    a = dist(middle, end)
    if abs(a) < 0.0001:
        return -1
    b = dist(start, middle)
    c = dist(start, end)
    frac = (a ** 2 + b ** 2 - c ** 2) / (2 * a * b)
    if frac > 1:
        frac = 1
    elif frac < -1:
        frac = -1
    angle = math.degrees(math.acos(frac))
    return angle

# normalise angle to 0->360 degrees
def norm_ang(angle):
    if angle < 0:
        angle = 360 + angle
    elif angle > 360:
        angle = angle - 360
    return angle

# checks if cell x, y is within the tracker's sight
def sight(tracker, x, y, angles, state, error):
#    l =dist([x, y], state)
#     print "dist:", l
#     print "x,y:",  x, y
    if abs(x-state[0]) > error or abs(y-state[1]) > error:
        if x >= 0 and x <= 1 and y >= 0 and y <= 1:
            if dist([x, y], state) <= (tracker.params[-1]+error):
                a = angle([state[0] + 1.0, state[1]], [state[0], state[1]], [x, y])
                if a > -0.1:
                    if y < state[1]:
                        a = -a
    #                 print "angles:", angles
    #                 print "a:", a
                    if a <= angles[0] and a >= angles[1]:
    #                 if abs(tracker.state[2]-a)<= tracker.params[-2]:
    #                     print "appended"
                        return True
    return False

# vision function which returns visible cells for person, different between target and tracker
def vision(person, state, type): 
    error = 0.00001
    # type is set to True for Tracker, False for target
    if type == True:
        step = 1.0 / person.m
        xoff = abs((state[0] % step) - (step / 2))
        yoff = abs((state[1] % step) - (step / 2))
#     print step
    else:
        step = 1.0/ (2.0*person.m)
        xoff = 0
        yoff = 0

    number = int(person.params[-1] / step)+1
    
#     print number
    
    if xoff < error and yoff < error:
        points = [[state[0], state[1]]]
    else:
        points = []
#     print "off: %.2f %.2f" % (xoff, yoff)
    angles = [state[2] + (person.params[-2] / 2), state[2] - (person.params[-2] / 2)]
    
    for i in range(int(number-xoff)):
        xstep = xoff + step * i
        for j in range(int(number-yoff)):
            ystep = yoff + step * j
#             print "step: %.5f %.5f" % (xstep, ystep)
#                 print person.state
                
            tempx = state[0] + xstep
            tempy = state[1] + ystep
#                 print "temp: %.2f %.2f" % (tempx, tempy)
            if sight(person, tempx, tempy, angles, state, error)==True:
                points.append([tempx, tempy])
                
            if abs(xstep) > error:
                tempx = state[0] - xstep
                tempy = state[1] + ystep
#                 print "temp: %.2f %.2f" % (tempx, tempy)
                if sight(person, tempx, tempy, angles, state, error)==True:
                    points.append([tempx, tempy])
            
            if abs(xstep) > error and abs(ystep) > error:
                tempx = state[0] - xstep
                tempy = state[1] - ystep
#                 print "temp: %.2f %.2f" % (tempx, tempy)
                if sight(person, tempx, tempy, angles, state, error)==True:
                    points.append([tempx, tempy])
            
            if abs(ystep) > error:
                tempx = state[0] + xstep
                tempy = state[1] - ystep
#                 print "temp: %.2f %.2f" % (tempx, tempy)
                if sight(person, tempx, tempy, angles, state, error)==True:
                    points.append([tempx, tempy])
    
    return points


# function used to check if person1 can see person2, returns a list of reward points

def check(p1, p2, person1, person2):
    # check if person1 can see person2
    # return 1 if can
    p3 = [p1[0]+1, p1[1]] #position along the xaxis from p2
    direction = float(p1[2])
    
    x,y = p2[0] - p1[0], p2[1] - p1[1]
    dist = np.sqrt(x**2 + y**2)
    R = person1.params[-1]
    if dist <= R+0.001:
        angle = angle_about_mid(p3,p1,p2)
        if 0.001>(p3[1] - p1[1])>(-0.001) and 0.001>(p2[1] - p1[1])>(-0.001):
            if p3[0]>p1[0]>p2[0]:
                angle = np.pi 
        if round(ccw(p3,p1,p2),3) <  0:
            direction = 360 - direction
            if (direction - person1.params[-2]/2 - 0.001) <= np.rad2deg(angle) and (direction + person1.params[-2]/2+ 0.001) >= np.rad2deg(angle):
                return 1 
        if (direction - person1.params[-2]/2 - 0.001) <= np.rad2deg(angle) and (direction + person1.params[-2]/2 + 0.001) >= np.rad2deg(angle):
            return 1
    return 0

def suitable_state(person, step):
    # make sure state is still within bounds
    if person.state[0] > 1 or person.state[0] < 0 or person.state[1] > 1 or person.state[1] < 0:
        return False 
    
#     if person.state[0] > 1:
#         person.state[0] = 1 - (step / 2)
#     elif person.state[0] < 0:
#         person.state[0] = 0 + (step / 2)
#     if person.state[1] > 1:
#         person.state[1] = 1 - (step / 2)
#     elif person.state[1] < 0:
#         person.state[1] = 0 + (step / 2)

    # check is person is inside an obstacle
    for i in person.obstacles:
        if point_in_polygon(i, person.state):
            return False

    return True
