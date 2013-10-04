import numpy as np
import math
from vectors import *

class Tracker:
    def __init__(self, num, policy, goal, targetParam, targetState, params, state, obstacles, C):
        self.num = num
        self.policy = policy
        self.goal = goal
        self.targetParam = targetParam
        self.targetMotion = None
        self.targetState = targetState
        self.motionHist = None
        self.params = params #[minLength, maxLength, beta, R] or [beta, R]
        self.state = state #[x,y,theta, c(length of camera)]
        self.obstacles = obstacles
        self.C = C
        
class Target:
    def __init__(self, num, policy, goal, targetParam, targetState, obstacles, A):
        self.num = num
        self.policy = policy
        self.goal = goal
        self.params = targetParam #[alpha, R]
        self.motionHist = None
        self.state = targetState #[x,y,theta]
        self.obstacles = obstacles
        self.A = A
        
def target_motion_history(file_i):
    data = open(file_i, 'r')
    lines = data.readlines()
    init = float(lines.pop(0).strip('\r\n'))
    count = 0.0
    for line in lines:
        if line[0] == line[2]:
            count += 1
    print count/init
    # do stuff
    
    
    
    data.close()
        
# function used to determine the divergence probability from previous data Stohcastic model
def tracker_motion_history(file):
    data = open(file, 'r')
    lines = data.readlines()
    action = [0, 0, 0, 0, 0, 0, 0, 0]
    prob_map = []
    for i in range(int(lines[0].strip('\n').strip('\r'))):
        data1 = lines[1 + i].strip('\n').strip('\r').split(' ')
    # do stuff
    
    data.close()
    return prob_map


# function used to diverge person based on probability of motion history
def diverge(person):
    # check desired action and generate random number, map probability to random number to get position
    pass
    

def finish(goal, target_pos):
    
    # check is target has reached goal
    return False

# Function used to determine which cells can be observed by the tracker at its state
def observation(tracker):
    cells = []
    
    
    return cells

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
            

