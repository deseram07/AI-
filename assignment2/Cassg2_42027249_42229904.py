import sys
import numpy as np
from Cutilities import *
import random

debug = 0
# debug = "target" # used for debugging target moves


def tracker_turn(tracker):
    obs = observation(tracker)
    previous_state = tracker.state[:]
    step = 1.0 / tracker.m
    
    ##### Do everything else ------------------------------------------------------------------------
    
    if suitable_state(tracker, step)==False:
        tracker.state = previous_state
    pass

def target_turn(target):
    step = 1.0 / target.m
    if debug == "target":
        print "step: " + str(step) + "\t gridLoc: " + str(int(target.state[1] / step)) + ", " + str(int(target.state[0] / step))
    action = target.policy[int(target.state[1] / step)][int(target.state[0] / step)]
    if debug == "target":
        print "policy: " + str(action)
    rand = random.random()
    if(target.A == 1):  # A1 -----------------------------------------------
        action = random.randint(0, 8)
    else:  # A2 -----------------------------------------------------------
        prob = 0.0
        for i in range(len(target.motionHist)):
            prob += target.motionHist[action][i]
            if(rand < prob):
                action = i
                break
    
    # perform action for target
    state = target.state[:]
    if action < 3:
        target.state[1] += step
    elif action > 5:
        target.state[1] -= step
    if action % 3 == 0:
        target.state[0] -= step
    elif action % 3 == 2:
        target.state[0] += step
        
    if (suitable_state(target, step)==False):
        action = 4
        target.state = state
        
#     flag = 0
#     # make sure state is still within bounds
#     if target.state[0] > 1:
#         flag = 1
#         target.state[0] = 1 - (step / 2)
#     elif target.state[0] < 0:
#         flag = 1
#         target.state[0] = 0 + (step / 2)
#     if target.state[1] > 1:
#         flag = 1
#         target.state[1] = 1 - (step / 2)
#     elif target.state[1] < 0:
#         flag = 1
#         target.state[1] = 0 + (step / 2)
#         
#     for i in target.obstacles:
#         if point_in_polygon(i, target.state):
#             target.state = state
#             action = 4
#             break
#         
#     if flag == 1:
#         action = 4
#         target.state = state
    
    if debug == "target":
        print "action: " + str(action)
    

"""
function for controlling the game
"""
def play_game(tracker, target, outputfile):
    turn = 0
    trackerPoints = 0
    targetPoints = 0
    targetPos = tracker.targetState
    list = ["%s" % str(i) for i in tracker.state]
    hist = [' '.join(list)]
    list = ["%s" % str(i) for i in target.state]
    string = ' '.join(list)
    hist.append(string)
    print hist
    if debug == "target":
        print target.goal
        print target.state
#     for i in range(target.num):
#         hist.append(' '.join(targetPos[i]))
    while(finish(tracker.goal, targetPos) == False):
        if (turn % 2 == 0):
            pass
#             tracker_turn(tracker) # action
#             diverge(tracker)
#             reward = check(tracker, target) # observation
#             if reward == 1:
#                 tracker.targetState = target.state
#             trackerPoints += reward
#             list = ["%.s"% str(i) for i in tracker.state]
#             string = ' '.join(list) + ' ' + str(reward)
#             string = ' '.join(tracker.state) + ' ' + str(reward[0])
#             hist.append(string)

        else:
            if debug == "target":
                print target.goal
                print target.state
                raw_input("Press Enter to continue...")
            target_turn(target)
#             if debug == "target":
#                 print target.goal
#                 print target.state
#                 raw_input("Press Enter to continue...")
#             reward = check(target, tracker)
            reward = 0
            targetPoints += reward
            list = ["%s" % str(i) for i in target.state]
            string = ' '.join(list) + ' ' + str(reward)
            hist.append(string)
            targetPoints = targetPoints + reward
            hist.append(string)
            
        turn += 1

#     print hist
#     output = open(outputfile, 'w')
#     output.close()

def main(inputfile, outputfile):
    path = 'tools/'
    obstacles = []
    targetsData = []
    
    """
    Read in setup file
    """
    setup = open(inputfile, 'r')
    lines = setup.readlines()
    t = int(lines[0].strip('\n').strip('\r'))
    A = int(lines[1].strip('\n').strip('\r')[-1])
    files = lines[2].strip('\n').strip('\r').split(' ')  # [target policy (, target motion history)]
    temp = lines[3].strip('\n').strip('\r').split(' ')
    targetParams = [float(temp[0]), float(temp[1])]
    if A == 2:
        targetsData = files[1]
        target_Prob = target_motion_history(path + targetsData)
    targetsPolicy = files[0]
    B = int(lines[4].strip('\n').strip('\r')[-1])
    if B == 2:
        trackerData = lines[5].strip('\n').strip('\r')
        tracker_Prob = tracker_motion_history(path + trackerData)
    C = int(lines[6].strip('\n').strip('\r')[-1])
    temp = lines[7].strip('\n').strip('\r').split(' ')  # [(minLength, maxLength,) beta, Rb]
    trackerParams = []
    for i in range(len(temp)):
        trackerParams.append(float(temp[i]))
    temp = lines[8].strip('\n').strip('\r').split(' ')  # [x, y, heading(, initialLength)]
    trackerPos = []
    for i in range(len(temp)):
        trackerPos.append(float(temp[i]))
    temp = lines[9].strip('\n').strip('\r').split(' ')
    targetsPos = [float(temp[0]), float(temp[1]), float(temp[2])]  # [x, y, heading]
    end = lines[9 + t].strip('\n').strip('\r').split(' ')
    x = sorted(end[::2])
    y = sorted(end[1::2])
    goal = [[float(x[0]), float(y[0])], [float(x[-1]), float(y[-1])]]  # [[minX, minY], [maxX, maxY]]
    
    # Creating obstacles in grid
    for j in range(int(lines[10 + t].strip('\n').strip('\r'))):
        obstacle = lines[10 + t + j + 1].strip('\n').strip('\r').split(' ')
        x = sorted(obstacle[::2])
        y = sorted(obstacle[1::2])
        obstacles.append([[float(x[0]), float(y[0])], [float(x[-1]), float(y[-1])]])  # [[[x1_low, y1_low], [x1_high, y1_high]],[....]]
    setup.close()
    
    """
    Read in target policy data, store in 2D list 
    """
    policyFile = open(path + targetsPolicy, 'r')
    lines = policyFile.readlines()
    temp = lines[0].strip('\n').strip('\r').split(' ')
    row = int(temp[0])
    column = int(temp[1])
    policyData = []
    for i in range(row):
        temp = lines[i + 1].strip('\n').strip('\r').strip('').split(' ')  # ref policyData[row][col]
        rowData = []
        for j in temp:
            if j.isdigit():
                rowData.append(int(j))
        policyData.insert(0, rowData)
#         policyData.append(rowData)
    if debug == "target":
        print policyData

        # 0 = NW, 1 = N, 2 = NE, 3 = W, 4 = stay, 5 = E, 6 = SW, 7 = S, 8 = SE.
    policyFile.close()
    
    
    """
    Create target and tracker
    """
    target = Target(row, 1, policyData, goal, targetParams, targetsPos, obstacles, A)
    tracker = Tracker(row, 1, policyData, goal, targetParams, targetsPos, trackerParams, trackerPos, obstacles, C)
    
    if A == 2:
        target.motionHist = target_Prob
        tracker.targetMotion = target_Prob
    if B == 2:
        tracker.motionHist = tracker_Prob
     
#     print target.obstacles
#     print target.goal
#     print target.state
# #     print target.policy
# #     print target.motionHist
#     sys.exit(0)
    """
    play game
    """
    play_game(tracker, target, outputfile)
    

    

if __name__ == '__main__':
    if(len(sys.argv) is not 3):
        print "Usage: python assg1_42027249_42229904.py desired_input_file desired_output_file"
        sys.exit(1)
    else:
        main(sys.argv[1], sys.argv[2])
        
        
    

