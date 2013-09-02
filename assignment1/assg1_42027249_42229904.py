import sys
# import numpy as np
# import math
from utility import *
import heapq
# import cv2

            
# gets distance from one sample configuration to another
def get_dist(sample, other):
    distx = []
    disty = []
    for i in range(len(sample.coords) / 2):
        distx.append(abs(sample.coords[i] - other.coords[i]))
        disty.append(abs(sample.coords[i + 1] - other.coords[i + 1]))
    distx.sort(reverse=True)
    disty.sort(reverse=True)
    return distx[0] + disty[0]

# converts back to given workspace
def get_decimal(coords):
    points = []
    for i in range(len(coords)):
        points.append(float(coords[i]) / 1000.0)
    return points

# output the path to file
def display_path(outputfile, sample):

#     print 'path found'
    path = []
#     print AStar.start.coords
    # creates path from the end to the start inserting into the beginning 
    while sample.parent is not AStar.start:
        coords = get_decimal(sample.coords)
        path.insert(0, coords)
        sample = sample.parent
    # inserts the start configuration into the path
    coords = get_decimal(AStar.start.coords)
    path.insert(0, coords)
    # outputs the path with the coordinates of each configuration separated by spaces
    xp = []
    yp = []
    for x in range(len(path)):
        if debug:
            for i in range(len(path[x])/2):
                xp.append(1000.0 * path[x][i*2])
                yp.append(1000.0 * path[x][i*2 + 1])
                ox1 = [0,200,200,0,0]
                ox2 = [500,700,700,500,500]
                oy1 = [200,200,400,400,200]
                oy2 = [600,600,900,900, 600]
            print xp, yp
            py.plot(ox1, oy1, '-+')
            py.plot(ox2, oy2, '-+')
            py.plot(xp, yp, '-+')
            py.show()
            xp = []
            yp = []
        outputfile.write(' '.join(map(str, path[x])))
        
# returns the estimated cost to destination from current position
def get_h(sample):
    dist = get_dist(sample, AStar.end)
#     (abs(sample.cx - AStar.end.cx) + abs(sample.cy - AStar.end.cy)) * 10 + abs(sample.angle - AStar.end.angle) / 10
    return dist

# returns samples from a given location
def get_samples(array, x, y):
    return array[y][x]

# updates adjacent sample with details from current sample
def update_sample(adj, sample):
    adj.g = sample.g + get_dist(sample, adj)
    adj.h = get_h(adj)
    adj.parent = sample
    adj.f = adj.g + adj.h
    
# get nearby samples based on centroid position
def get_adj(array, sample):
    samples = []
    movex = [0]
    movey = [0]
    # checks where to get samples from
    if sample.x < ((AStar.width / AStar.grid) - 1):
        movex.append(1)
    if sample.y > 0:
        movey.append(-1)
    if sample.x > 0:
        movex.append(-1)
    if sample.y < ((AStar.width / AStar.grid) - 1):
        movey.append(1)
    # gets samples from available grid squares
    for i in movex:
        for j in movey:
            samples.append(get_samples(array, sample.x + i, sample.y + j))
    return samples

# A* search processing
def process(cSpace, start, dest):
    array = [[[] for x in range(AStar.width / AStar.grid)] for y in range(AStar.width / AStar.grid)]
    # map samples to their positions in grid space via their centroid positions
    for i in cSpace:
#         print i
#         cx, cy, angle = centroid_angle(i)
        cx, cy = centroid_angle(i)
        array[cy / AStar.grid][cx / AStar.grid].append(Sample(i, cx, cy, cx / AStar.grid, cy / AStar.grid))#, angle))
    
    # add end position to samples
#     cx, cy, angle = centroid_angle(dest)
    cx, cy = centroid_angle(dest)
    AStar.end = Sample(dest, cx, cy, cx / AStar.grid, cy / AStar.grid)#, angle)
    array[cy / AStar.grid][cx / AStar.grid].append(AStar.end)
    
    # create start position sample
#     cx, cy, angle = centroid_angle(start)
    cx, cy = centroid_angle(start)
    AStar.start = Sample(start, cx, cy, cx / AStar.grid, cy / AStar.grid)#, angle)
    AStar.start.h = get_h(AStar.start)
    AStar.start.f = AStar.start.g + AStar.start.f
    
    # start A* search
    heapq.heappush(AStar.op, (AStar.start.f, AStar.start))
    while len(AStar.op):
#         print 'searching'
        # get sample from the open list based on samples f value
        f, sample = heapq.heappop(AStar.op)
        AStar.cl.add(sample)
#         print sample.coords
#         print AStar.end.coords
        for i in range(len(sample.coords)):
            if sample.coords[i] != AStar.end.coords[i]:
                break
            elif i == len(sample.coords)-1:
                return sample
        # check if it's the final position
#         if sample.coords == AStar.end.coords:
#             return sample
        # get samples which are near to the current
        adj_samples = get_adj(array, sample)
        for c in adj_samples:
            for d in c:
                if d not in AStar.cl:
                    if (d.f, d) in AStar.op:
                        if d.g > (sample.g + get_dist(sample, d)):
                            update_sample(d, sample)
                    else:
                        update_sample(d, sample)
                        heapq.heappush(AStar.op, (d.f, d))
    return False            
        

def main(inputfile, outputfile):
    global minArea
    global AStar
    obstacles = []
    cSpace = []
    AStar = Astar()
    grid = np.zeros(shape=(1000, 1000))
    file = open(inputfile, 'r')
    output = open(outputfile, 'w')
    lines = file.readlines()
    start = remove_decimal(lines[1].strip('\n').split(' '))
    finish = remove_decimal(lines[2].strip('\n').split(' '))

    asv = []
    number = int(lines[0].strip('\n'))
    for i in range(number):
        # Create and initialise ASVs
        asv.append(ASV(i, start[i * 2], start[i * 2 + 1], finish[i * 2], finish[i * 2 + 1]))
        if i is not 0:
            asv[i].boom = start[-(number - i)]
    asv[0].direction = ccw(asv[0], asv[1], asv[2])
    
#    src = cv2.cv.fromarray(grid)
#    cv2.cv.ShowImage('win1', src)
#    cv2.waitKey()

    # Creating obstacles in grid
    for j in range(int(lines[3].strip('\n'))):
        obstacle = remove_decimal(lines[j + 4].strip('\n').split(' '))
        obstacles.append(obstacle)
        final_obstacle = [obstacle[1], obstacle[5] + 1, obstacle[0], obstacle[4] + 1]
        index = 0
        while index < len(final_obstacle):
            if final_obstacle[index] < 0:
                final_obstacle[index] = 0
            index += 1 
        grid[final_obstacle[0]:final_obstacle[1], final_obstacle[2]:final_obstacle[3]] = 1
    
    i = 1
    cSpace = obtain_random_points(asv, 5000, obstacles, grid )
    end = process(cSpace, start[:-number+1], finish[:-number+1])
    while end == False:
        print 'trying again'
        cSpace = obtain_random_points(asv, 5000*i*5, obstacles, grid )
        end = process(cSpace, start[:-number+1], finish[:-number+1])
        i+=1
    display_path(output, end)
    output.close()
    file.close()

if __name__ == '__main__':
    if(len(sys.argv) is not 3):
        print "Usage: python assg1_42027249_42229904.py desired_input_file desired_output_file"
        sys.exit(1)
    else:
        main(sys.argv[1], sys.argv[2])
    

