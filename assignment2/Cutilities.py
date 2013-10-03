import numpy as np

class Tracker:
    def __init__(self, m, num, policy, goal, targetParam, targetState, params, state, obstacles, C):
        self.m = m # grid size, ie number of rows or number of columns
        self.num = num # number of targets
        self.policy = policy # array[m][m] = 0->8 actions
        self.goal = goal # finish area [[minx, miny], [maxx, maxy]]
        self.targetParam = targetParam # [alpha, ra]
        self.targetMotion = None # probability map array[action][outcome]
        self.targetState = targetState # [x, y, theta]
        self.motionHist = None # probability map array[action][outcome]
        self.params = params #[(minLength, maxLength,) beta, rb]
        self.state = state #[x, y, theta (, length)]
        self.obstacles = obstacles #[[[minx, miny], [maxx, maxy]],[....]]
        self.desiredAction = None 
        self.C = C # int 0 for using eyes, 1 for using camera on stick
        
class Target:
    def __init__(self, m, num, policy, goal, targetParam, targetState, obstacles, A):
        self.m = m # grid size, ie number of rows or number of columns
        self.num = num # number of targets
        self.policy = policy # array[m][m] = 0->8 actions
        self.goal = goal # finish area [[minx, miny], [maxx, maxy]]
        self.params = targetParam # [alpha, ra]
        self.motionHist = None # probability map array[action][outcome]
        self.state = targetState # [x, y, theta]
        self.obstacles = obstacles #[[[minx, miny], [maxx, maxy]],[....]]
        self.A = A # movement type, 0 completely random, 1 modeled random

        
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
#     print 'finish'
    return point_in_polygon(goal, target_pos)

# check in coordinate is inside polygon (works for state inside polygon)
def point_in_polygon(polygon, point):
    # polygon = [[minX, minY], [maxX, maxY]], point = [x, y]
#     print 'poi',point[0]
#     print 'ploy',polygon
    if point[0] >=  polygon[0][0] and point[0] <= polygon[1][0] and polygon[0][1] <= point[1] and point[1] <= polygon[1][1]:
        return True
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

def suitable_state(person, step):
    flag = 0
    # make sure state is still within bounds
    if person.state[0] > 1 or person.state[0] < 0 or person.state[1] > 1 or person.state[1] < 0:
        return False 
#     if person.state[0] > 1:
#         flag = 1
#         person.state[0] = 1 - (step / 2)
#     elif person.state[0] < 0:
#         flag = 1
#         person.state[0] = 0 + (step / 2)
#     if person.state[1] > 1:
#         flag = 1
#         person.state[1] = 1 - (step / 2)
#     elif person.state[1] < 0:
#         flag = 1
#         person.state[1] = 0 + (step / 2)
    # check is person is inside an obstacle
    for i in person.obstacles:
        if point_in_polygon(i, person.state):
            return False

#     if flag == 1:
#         return False
    return True