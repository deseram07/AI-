import sys
import numpy as np
from utilities import *

def tracker_turn():
    pass

def target_turn():
    pass

"""
function for controlling the game
"""
def play_game():
    turn = 0
    hist = []
    while(finish(goal, target_position)==False):
        if (turn%2==0):
            tracker_turn()
            trackPoints = trackPoints + check(tracker, target)
            hist.append(tracker, reward)
        else:
            target_turn()
            targetPoints = targetPoints + check(target, tracker)
            hist.append(target)
        turn += 1
    return turn

def main(inputfile, outputfile):
    path = 'tools/'
    obstacles = []
    obstacle_x = []
    obstacle_y = []
    targetsPolicy = []
    targetsData = []
    targetsPos = []
    alpha = []
    Ra = []
#     grid = np.zeros(shape=(1000, 1000)) ## set this later  ------- --- -- --- -- - -
    file = open(inputfile, 'r')
#     output = open(outputfile, 'w')
    lines = file.readlines()
    t = int(lines[0].strip('\n').strip('\r'))
    A = int(lines[1].strip('\n').strip('\r')[-1])
    files = lines[2].strip('\n').strip('\r').split(' ')  # [target policy (, target motion history)]
    params = lines[3].strip('\n').strip('\r').split(' ')
    if A == 2:
        targetsData = files[1]
        target_Prob = motion_history(path+targetsData)
    targetsPolicy = files[0]
    for i in range(t / 2):
        alpha.append(params[i * 2])
        Ra.append(params[i * 2 + 1])
    B = int(lines[4].strip('\n').strip('\r')[-1])
    if B == 2:
        trackerData = lines[5].strip('\n').strip('\r').split(' ')
        tracker_Prob = motion_history(path+trackerData)
    C = int(lines[6].strip('\n').strip('\r')[-1])
    trackerParams = lines[7].strip('\n').strip('\r').split(' ')  # [(minLength, maxLength,) beta, Rb]
#     if C == 2:
#         minLength = trackerParams[0]
#         maxLength = trackerParams[1]  #    Use this for only C1
#     beta = trackerParams[-2]
#     Rb = trackerParams[-1]
    
    trackerPos = lines[8].strip('\n').strip('\r').split(' ')  # [x, y, heading(, initialLength)]
    
    for i in range(t):
        targetsPos.append(lines[9 + i].strip('\n').strip('\r').split(' '))  # [x, y, heading, x, y, heading, ...]
    end = lines[9 + t].strip('\n').strip('\r').split(' ')
    x = sorted(end[::2])
    y = sorted(end[1::2])
    goal = [[x[0], y[0]], [x[-1], y[-1]]]  # [[minX, minY], [maxX, maxY]]
    
    # Creating obstacles in grid
    for j in range(int(lines[10 + t].strip('\n').strip('\r'))):
        obstacle = lines[10 + t + j + 1].strip('\n').strip('\r').split(' ')
        x = sorted(obstacle[::2])
        y = sorted(obstacle[1::2])
        obstacles.append([x[0], y[0], x[-1], y[-1]])  # [[x1_low, y1_low, x1_high, y1_high],[....]]
    file.close()
    """
    Read in target policy data, store in 2D list 
    """
    file = open(path+targetsPolicy, 'r')
    lines = file.readlines()
    temp = lines[0].strip('\n').strip('\r').split(' ')
    row = int(temp[0])
    column = int(temp[1])
    policyData = []
    for i in range(row):
        policyData.append(lines[i+1].strip('\n').strip('\r').split(' ')) #ref policyData[row][col]
        # 0 = NW, 1 = N, 2 = NE, 3 = W, 4 = stay, 5 = E, 6 = SW, 7 = S, 8 = SE.
    file.close()
    
#     output.close()
    

if __name__ == '__main__':
    if(len(sys.argv) is not 3):
        print "Usage: python assg1_42027249_42229904.py desired_input_file desired_output_file"
        sys.exit(1)
    else:
        main(sys.argv[1], sys.argv[2])
    

