import sys
import numpy as np
from Cutilities import *
import random
import vectors

debug = 0
# debug = "target" # used for debugging target moves


def tracker_turn(tracker, target):
    Value_init = np.zeros(24,dtype = np.float)  #Value function matrix for processing
    Value_processing = np.zeros(24,dtype = np.float)    #Value function matrix to update while processing
    
    obs = observation(tracker)
    previous_state = tracker.state[:]
    step = 1.0 / tracker.m

#    current possition of the target    
    targetx = target.state[0] / step
    targety =target.state[1] / step
    
    action = target.policy[int(targetx)][int(targety)]
    
#    displacement of target
    target_states = []
    tracker_states = []
    for i in target.actionspace:
        dx,dy = i
        target_states.append([target.state[0]+dx*step ,target.state[1]+dy*step, int(norm_ang(math.degrees(math.atan2(dy, dx))))])
        
#    displacement of tracker
    print tracker.state
    for i in tracker.actionspace:
        dx,dy = i
        tracker_states.append([tracker.state[0]+dx*step ,tracker.state[1]+dy*step, int(norm_ang(math.degrees(math.atan2(dy, dx))))])
    print tracker_states
#    print tracker.Value
    
#    initial update of value function using trackers new position
#    assigning negative values for what target can see
    
    prob = target.motionHist[action]
#    print target.state
#    print tracker_states,'\n'
    for i in range(len(prob)):
        cells = vision(target,target_states[i], False)
        for j in range(len(tracker_states)):
            check = tracker_states[j][:2]
            for c in cells:
                if abs(c[0] - check[0]) < 0.0001 and (abs(c[1] - check[1]) < 0.0001):
                    Value_init[j] -= prob[i]*(1.0)
#    print Value_init
        
    ##### Do everything else ------------------------------------------------------------------------
    
    if suitable_state(tracker, step) == False:
        tracker.state = previous_state
    pass

def target_turn(target):
    step = 1.0 / target.m
    if debug == "target":
        print "step: " + str(step) + "\t gridLoc: " + str(int(target.state[1] / step)) + ", " + str(int(target.state[0] / step))
    action = target.policy[int(target.state[1] / step)][int(target.state[0] / step)]
    if debug == "target":
        print "policy: " + str(action)
    
    if(target.A == 1):  # A1 -----------------------------------------------
        action = random.randint(0, 8)
    else:  # A2 -----------------------------------------------------------
        rand = random.random()
        prob = 0.0
        for i in range(len(target.motionHist)):
            prob += target.motionHist[action][i]
#             print prob
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
        
    if (suitable_state(target, step) == False):
        action = 4
        target.state = state
    
    if action < 3:
        target.state[2] = 45 * (3 - action)
    elif action == 3:
        target.state[2] = 180
    elif action == 5:
        target.state[2] = 0
    elif action > 5:
        target.state[2] = 180 + 45 * (action - 5)
    
    if debug == "target":
        print "action: " + str(action)

"""
function for controlling the game
"""
def play_game(tracker, target, outputfile):
    turn = 0
    trackerPoints = 0
    targetPoints = 0
#     targetPos = tracker.targetState
    list = ["%s" % str(i) for i in tracker.state]
    hist = [' '.join(list)]
    list = ["%s" % str(i) for i in target.state]
    string = ' '.join(list)
    hist.append(string)
#     print hist
# #     if debug == "target":
# #         print target.goal
# #         print target.state
#     for i in range(target.num):
#         hist.append(' '.join(targetPos[i]))
    while(finish(tracker.goal, target.state) == False):
        if (turn % 2 == 0):
#            pass
            tracker_turn(tracker, target) # action
            sys.exit()
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
#                 print target.goal
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
#     if debug == "target":
#         print policyData

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
        
        
    

