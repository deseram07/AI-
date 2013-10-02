import numpy as np

def motion_history(file):
    data = open(file, 'r')
    lines = data.readlines()
    init = float(lines.pop(0).strip('\r\n'))
    count = 0.0
    for line in lines:
        if line[0] == line[2]:
            count += 1
    print count/init
    # do stuff
    prob_map = 0
    return prob_map

def finish(goal, target_pos):
    
    # check is target has reached goal
    return False

def check(person1, person2):
    #check if person1 can see person2
    #return 1 if can
    return 0