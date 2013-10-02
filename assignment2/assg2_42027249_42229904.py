import sys
import numpy as np
from utilities import *

def tracker_turn(tracker):
    obs = observation(tracker)
    pass

def target_turn(target):
    
    pass

"""
function for controlling the game
"""
def play_game(tracker, target, outputfile):
    turn = 0
    trackerPoints = 0
    targetPoints = 0
    targetPos = tracker.targetState
    hist = [' '.join(tracker.state)]
    for i in range(target.num):
        hist.append(' '.join(targetPos[i]))
    while(finish(tracker.goal, targetPos) == False):
        if (turn % 2 == 0):
            
            tracker_turn() # action
            diverge(tracker)
            reward = check(tracker, target) # observation
            trackerPoints = trackerPoints + reward[0]
            string = ' '.join(tracker.state) + ' ' + str(reward[0])
            hist.append(string)
        else:
            target_turn(target)
            reward = check(target, tracker)
            diverge(target)
            for i in range(target.num):
                string = ' '.join(targetPos[i]) + ' ' + str(reward[i])
                hist.append(string)
            
            print string
            targetPoints = targetPoints + reward
            hist.append(string)
        turn += 1
#     output = open(outputfile, 'w')
#     output.close()

def main(inputfile, outputfile):
    path = 'tools/'
    obstacles = []
    targetsPolicy = []
    targetsData = []
    targetsPos = []
    alpha = []
    Ra = []
    
    """
    read in setup file
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
#     for i in range(t):
#         targetsPos.append(lines[9 + i].strip('\n').strip('\r').split(' '))  # [x, y, heading, x, y, heading, ...]
    temp = lines[9].strip('\n').strip('\r').split(' ')
    targetsPos = [float(temp[0]), float(temp[1]), float(temp[2])]
    end = lines[9 + t].strip('\n').strip('\r').split(' ')
    x = sorted(end[::2])
    y = sorted(end[1::2])
    goal = [[float(x[0]), float(y[0])], [float(x[-1]), float(y[-1])]]  # [[minX, minY], [maxX, maxY]]
    
    # Creating obstacles in grid
    for j in range(int(lines[10 + t].strip('\n').strip('\r'))):
        obstacle = lines[10 + t + j + 1].strip('\n').strip('\r').split(' ')
        x = sorted(obstacle[::2])
        y = sorted(obstacle[1::2])
        obstacles.append([float(x[0]), float(y[0]), float(x[-1]), float(y[-1])])  # [[x1_low, y1_low, x1_high, y1_high],[....]]
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
        policyData.append(lines[i + 1].strip('\n').strip('\r').split(' '))  # ref policyData[row][col]
        # 0 = NW, 1 = N, 2 = NE, 3 = W, 4 = stay, 5 = E, 6 = SW, 7 = S, 8 = SE.
    policyFile.close()
    print len(policyData)
    
    target = Target(t, policyData, goal, targetParams, targetsPos, obstacles, A)
    tracker = Tracker(t, policyData, goal, targetParams, targetsPos, trackerParams, trackerPos, obstacles, C)
    
    if A == 2:
        target.targetMotion = target_Prob
        tracker.targetMotion = target_Prob
    if B == 2:
        tracker.motionHist = tracker_Prob
    """
    End of class setup
    """
    check(tracker,target)
    """
    play game
    """
    play_game(tracker, target, outputfile)
    

if __name__ == '__main__':
    if(len(sys.argv) is not 3):
        print "Usage: python assg1_42027249_42229904.py desired_input_file desired_output_file"
#        sys.exit(1)
    else:
        main(sys.argv[1], sys.argv[2])
        
        
    

