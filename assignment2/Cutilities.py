import numpy as np
import math

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
        self.actionspace = []
        
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
        self.actionspace = [[1,-1],[1,0],[1,1],[0,-1],[0,0],[0,1],[-1,-1],[-1,0],[-1,1]]\

        
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
#     a = int(dist(middle, end)*1000)
#     b = int(dist(start, middle)*1000)
#     c = int(dist(start, end)*1000)
    a = dist(middle, end)
    b = dist(start, middle)
    c = dist(start, end)
#     print "temp:",end
#     print "len:",a, b, c
    frac = (a ** 2 + b ** 2 - c ** 2) / (2 * a * b)
#     print "frac:",frac
    if frac > 1:
        frac = 1
    elif frac < -1:
        frac = -1

    angle = math.degrees(math.acos(frac))
#     print "angle: " + str(angle)
    return angle

# normalise angle to 0->360 degrees
def norm_ang(angle):
    if angle < 0:
        angle = 360 + angle
    elif angle > 360:
        angle = angle - 360
    return angle

# checks if cell x, y is within the tracker's sight
def sight(tracker, x, y, angles, error):
    l =dist([x, y], tracker.state)
    print "dist:", l
    print "x,y:",  x, y
    if abs(x-tracker.state[0]) > error or abs(y-tracker.state[1]) > error:
        if x >= 0 and x <= 1 and y >= 0 and y <= 1:
            if dist([x, y], tracker.state) <= (tracker.params[-1]+0.00003):
                a = angle([tracker.state[0] + 1.0, tracker.state[1]], [tracker.state[0], tracker.state[1]], [x, y])
                if y < tracker.state[1]:
                    a = -a
                print "angles:", angles
                print "a:", a
                if a <= angles[0] and a >= angles[1]:
#                 if abs(tracker.state[2]-a)<= tracker.params[-2]:
                    print "appended"
                    return True
    return False

# returns a list of target grid cells within the trackers view
def tracker_vision(tracker):
#     error = 0.000001
    error = -1
    min = 0.000001
    step = 1.0 / tracker.m
#     print step
    number = int(tracker.params[-1] / step)+1
#     print number
    xoff = abs((tracker.state[0] % step) - (step / 2))
    yoff = abs((tracker.state[1] % step) - (step / 2))
#     print "off: %.2f %.2f" % (xoff, yoff)
    points = []
    angles = [tracker.state[2] + tracker.params[-2] / 2, tracker.state[2] - tracker.params[-2] / 2]
    
    for i in range(int(number-xoff)):
        xstep = xoff + step * i
        for j in range(int(number-yoff)):
            ystep = yoff + step * j
            print "step: %.5f %.5f" % (xstep, ystep)
#                 print tracker.state
                
            tempx = tracker.state[0] + xstep
            tempy = tracker.state[1] + ystep
#                 print "temp: %.2f %.2f" % (tempx, tempy)
            if sight(tracker, tempx, tempy, angles, error)==True:
                points.append([tempx, tempy])
                
            if abs(xstep) > min:
                tempx = tracker.state[0] - xstep
                tempy = tracker.state[1] + ystep
#                 print "temp: %.2f %.2f" % (tempx, tempy)
                if sight(tracker, tempx, tempy, angles, error)==True:
                    points.append([tempx, tempy])
            
            if abs(xstep) > min and abs(ystep) > min:
                tempx = tracker.state[0] - xstep
                tempy = tracker.state[1] - ystep
#                 print "temp: %.2f %.2f" % (tempx, tempy)
                if sight(tracker, tempx, tempy, angles, error)==True:
                    points.append([tempx, tempy])
            
            if abs(ystep) > min:
                tempx = tracker.state[0] + xstep
                tempy = tracker.state[1] - ystep
#                 print "temp: %.2f %.2f" % (tempx, tempy)
                if sight(tracker, tempx, tempy, angles, error)==True:
                    points.append([tempx, tempy])
    
    return points


# function used to check if person1 can see person2, returns a list of reward points
def check(person1, person2):
    # check if person1 can see person2
    # return 1 if can
    p1 = person1.state[:2] 
    p2 = person2.state[:2]
    p3 = [p1[0]+1, p1[1]] #position along the xaxis from p2
    direction = person1.state[2]
    reward = []
    
    x,y = p2[0] - p1[0], p2[1] - p1[1]
    dist = np.sqrt(x**2 + y**2)
    R = person1.params[-1]
    if dist < R:
        angle = angle_about_mid(p1, p2, p3)
        if p1[0]<p2[0]:
            # gets the right angle if greater than 90 degrees
            angle = np.rad2deg(np.pi - angle)
            
        if not ccw(p1,p2,p3):
            angle = -np.rad2deg(angle)
        if abs(direction - angle)>person1.params[-2]:
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
