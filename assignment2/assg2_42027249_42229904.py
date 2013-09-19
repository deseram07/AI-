import sys
import numpy as np

def main(inputfile, outputfile):
    obstacles = []
    obstacle_x = []
    obstacle_y = []
    targetsPolicy = []
    targetsData = []
    trackerData = []
    targetsPos = []
    alpha = []
    Ra = []
#     grid = np.zeros(shape=(1000, 1000)) ## set this later  ------- --- -- --- -- - -
    file = open(inputfile, 'r')
    output = open(outputfile, 'w')
    lines = file.readlines()
    t = int(lines[0].strip('\n'))
    A = int(lines[1][-1].strip('\n'))
    files = lines[2].strip('\n').split(' ')
    params = lines[3].strip('\n').split(' ')
    for i in range(t):
        if A == 2:
            targetsData.append(files[i * 2 + 1])
        targetsPolicy.append(files[i * 2])
        alpha.append(params[i * 2])
        Ra.append(params[i * 2 + 1])
    B = int(lines[4][-1].strip('\n').split(' '))
    if B == 2:
        trackerData.append(lines[5].strip('\n').split(' '))
        
    C = int(lines[6][-1].strip('\n').split(' '))
    minLength = 0
    MaxLength = 0
    trackerParams = lines[7].strip('\n').split(' ')  # [(minLength, maxLength,) beta, Rb]
#     if C == 2:
#         minLength = trackerParams[0]
#         maxLength = trackerParams[1]  #    Use this for only C1
#     beta = trackerParams[-2]
#     Rb = trackerParams[-1]
    
    trackerPos = lines[8].strip('\n').split(' ')  # [x, y, heading(, initialLength)]
    
    for i in range(t):
        targetsPos.append(lines[9 + i].strip('\n').split(' '))  # [x, y, heading, x, y, heading, ...]
    
    end = lines[9 + t].strip('\n').split(' ')
    x = sorted(end[::2])
    y = sorted(end[1::2])
    goal = [[x[0], y[0]], [x[-1], y[-1]]]  # [[minX, minY], [maxX, maxY]]
    
    # Creating obstacles in grid
    for j in range(int(lines[10 + t].strip('\n'))):
#         obstacle = remove_decimal(lines[j + 4].strip('\n').split(' '))
#         obstacles.append(obstacle)
        obstacles = lines[10 + t + j].strip('\n').split(' ')

    for i in obstacles:
        x = sorted(i[::2])
        y = sorted(i[1::2])
        obstacle_x.append([x[0], x[-1]])  # [[x_low, x_high],[x1_low, x1_high]]
        obstacle_y.append([y[0], y[-1]])




    
    output.close()
    file.close()

if __name__ == '__main__':
    if(len(sys.argv) is not 3):
        print "Usage: python assg1_42027249_42229904.py desired_input_file desired_output_file"
        sys.exit(1)
    else:
        main(sys.argv[1], sys.argv[2])
    

