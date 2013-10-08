import sys
import numpy as np
from utilities import *
import random
import vectors

debug = 0
# debug = "target" # used for debugging target moves


def tracker_turn(tracker, target):
    
    step = 1.0 / tracker.m
#    check if tracker can see target before moving
    if check(tracker.state, target.state, tracker, target):
#        update tracker.targetstate
        tracker.targetState = target.state[:]
    else:
        action = target.policy[int(tracker.targetState[0])][int(tracker.targetState[1])]
#        print action
        target_action = target.motionHist[action]
        target_states = []
        target_seen = []
        prob = []
        update_prob = []
        sum = 0.0
        for i in range(len(target.actionspace)):
            if target_action[i]>0:
#                if theres a probability of greater than 0 to move to a spot, updates target_states
                dx,dy = target.actionspace[i]
                target_states.append([tracker.targetState[0]+dx*step , tracker.targetState[1]+dy*step, int(norm_ang(math.degrees(math.atan2(dy, dx)))), target_action[i]])
                
        for i in range(len(target_states)):
#            from the possible positions that the targeted would have moved, this loop checks which ones the 
#            tracker can see and if it cant be seen, the probability of moving to that position is stored
            if check(tracker.state, target_states[i][:-1], tracker, target):
                pass
            else:
                if(suitable_state(target, target_states[i], step)):
                    prob.append([target_states[i][-1],i])
                    sum += target_states[i][-1]
        target_possible_action = random.random()
        prob.sort()
        for i in prob:
            update_prob.append(i[0]/sum)
        for i in range(len(update_prob)):
            if target_possible_action < update_prob[i]:
                tracker.targetstate = target_states[prob[i][-1]][:-1]
#        print tracker.targetstate
            
            
    Value_init = np.zeros(25,dtype = np.float)  #Value function matrix for processing
    Value_processing = np.zeros(25,dtype = np.float)    #Value function matrix to update while processing
    
    obs = observation(tracker)
    previous_state = tracker.state[:]
    

#    current possition of the target    
    targetx = tracker.targetState[0] / step
    targety =tracker.targetState[1] / step
    
    action_target = target.policy[int(targetx)][int(targety)]

#    displacement of target
    target_states = []
    tracker_states = []
    for i in target.actionspace:
        dx,dy = i
        target_states.append([target.state[0]+dx*step ,target.state[1]+dy*step, int(norm_ang(math.degrees(math.atan2(dy, dx))))])
        
#    displacement of tracker
    for i in tracker.statespace:
        dx,dy = i
        tracker_states.append([tracker.state[0]+dx*step ,tracker.state[1]+dy*step, int(norm_ang(math.degrees(math.atan2(dy, dx))))])
    
#    initial update of value function using trackers new position
#    assigning negative values for what target can see
    
    prob_target = target.motionHist[action_target]
    for i in range(len(prob_target)):
        for j in range(len(tracker_states)):
            if check(target_states[i], tracker_states[j], target,tracker):
                Value_init[j] -= (1.0) * prob_target[i]
            if check(tracker_states[j], target_states[i], tracker, target):
                Value_init[j] += (1.0)

#     print Value_init
    
# updating initial value function matrix with actions
    for action in tracker.actionspace:
        prob_tracker = tracker.motionHist[action]
        for i in range(len(prob_tracker)):
            Value_init[i] += (Value_init[i] * prob_tracker[i])
#            print Value_init
#        break
#     print Value_init
    
    best_action = 1
    for index in tracker.actionspace:
        if Value_init[index] > Value_init[best_action]:
            best_action = index
#     print best_action
#     print tracker_states[best_action]

    
    rand = random.random()
    possible = 0.0
    for i in range(len(tracker.motionHist)):
        possible += tracker.motionHist[best_action][i]
#             print prob
        if(rand < possible):
            act = i
            break

    if suitable_state(tracker, tracker_states[act], step):
        tracker.state = tracker_states[act]


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
    x,y = target.actionspace[action]
    state[0] = state[0] + x*step
    state[1] = state[1] + y*step
    state[2] = norm_ang(math.degrees(math.atan2(y, x)))
        
    if (suitable_state(target, state, step)):
        target.state = state[:]
    
    
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
            tracker_turn(tracker, target) # action
#            print tracker.state
#             diverge(tracker)
            reward = check(tracker.state, target.state, tracker, target) # observation
            if reward == 1:
                tracker.targetState = target.state[:]
            trackerPoints += reward
            list = ["%s"% str(i) for i in tracker.state]
            string = ' '.join(list) + ' ' + str(reward)
#             string = ' '.join(tracker.state) + ' ' + str(reward[0])
            hist.append(string)

        else:
            if debug == "target":
#                 print target.goal
                print target.state
                raw_input("Press Enter to continue...")
#             print target.state
            target_turn(target)
#             if debug == "target":
#                 print target.goal
#                 print target.state
#                 raw_input("Press Enter to continue...")
            reward = check(target.state, tracker.state, target, tracker)
#            print target.state
#             reward = 0
            targetPoints += reward
            list = ["%s" % str(i) for i in target.state]
            string = ' '.join(list) + ' ' + str(reward)
            hist.append(string)
            targetPoints = targetPoints + reward
#             hist.append(string)
#             sys.exit()te is stil
            
        turn += 1

    for i in range(len(hist)):
        print hist[i]
    output = open(outputfile, 'w')
    output.write(str(turn)+"\r\n")
    output.write('1\r\n')
    for i in range(len(hist)):
        output.write(hist[i])
        output.write("\r\n")
    output.close()

def main(inputfile, outputfile, folder):
    path = folder + '/'
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
        print temp[i]
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
    if(len(sys.argv) is not 4):
        print "Usage: python assg1_42027249_42229904.py setup_file desired_output_file folder_name/path"
        sys.exit(1)
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
        
        
    

