import numpy as np

class Tracker:
    def __init__(self, num, policy, goal, targetParam, targetState, params, state, obstacles, C):
        self.num = num
        self.policy = policy
        self.goal = goal
        self.targetParam = targetParam
        self.targetMotion = None
        self.targetState = targetState
        self.motionHist = None
        self.params = params
        self.state = state
        self.obstacles = obstacles
        self.C = C
        
class Target:
    def __init__(self, num, policy, goal, targetParam, targetState, obstacles, A):
        self.num = num
        self.policy = policy
        self.goal = goal
        self.params = targetParam
        self.motionHist = None
        self.state = targetState
        self.obstacles = obstacles
        self.A = A
        
def target_motion_history(file):
    data = open(file, 'r')
    lines = data.readlines()
    action = [0, 0, 0, 0, 0, 0, 0, 0]
    prob_map = []
    for i in range(int(lines[0].strip('\n').strip('\r'))):
        data = lines[1 + i].strip('\n').strip('\r').split(' ')
    # do stuff
    
    
    
    data.close()
    return prob_map
        
# function used to determine the divergence probability from previous data Stohcastic model
def tracker_motion_history(file):
    data = open(file, 'r')
    lines = data.readlines()
    action = [0, 0, 0, 0, 0, 0, 0, 0]
    prob_map = []
    for i in range(int(lines[0].strip('\n').strip('\r'))):
        data = lines[1 + i].strip('\n').strip('\r').split(' ')
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
    reward = []
    for i in len(person1.state):
        for j in len(person2.state):
            pass
            # # check vision
    return reward
