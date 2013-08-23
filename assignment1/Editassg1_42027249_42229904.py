import sys
# import numpy as np
# import math
from utilityedit import *
import heapq
# import cv2

# Working on grid (1000 x 1000) where obstacles are represented by 1s and clear is represented by 0s

# def init_grid(grid):
# #     array = [[[] for x in range(AStar.width / AStar.grid)] for y in range(AStar.width / AStar.grid)]
# #     x = 0
# #     y = 0
#     for x in range(AStar.width / AStar.grid):
#         for y in range(AStar.width / AStar.grid):
#             if grid[y][x] == 1:
#                 reachable = False
#             else:
#                 reachable = True
#             AStar.cells.append(Cell(x, y, reachable))

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
        points.append(coords[i] / 1000)
    return points

# output the path to file
def display_path(outputfile):
#     print 'path found'
    sample = AStar.end
    path = []
    # creates path from the end to the start inserting into the beginning 
    while sample.parent is not AStar.start:
        coords = get_decimal(sample.coords)
        path.insert(0, coords)
        sample = sample.parent
    # inserts the start configuration into the path
    coords = get_decimal(AStar.start.coords)
    path.insert(0, coords)
    # outputs the path with the coordinates of each configuration separated by spaces
    for x in range(len(path)):
        outputfile.write(' '.join(map(str, path[x])))
        
# returns the estimated cost to destination from current position
def get_h(sample):
    dist = get_dist(sample, AStar.end)
#     (abs(sample.cx - AStar.end.cx) + abs(sample.cy - AStar.end.cy)) * 10 + abs(sample.angle - AStar.end.angle) / 10
    return dist

# returns samples from a given location
def get_samples(x, y):
    return array[y][x]

# updates adjacent sample with details from current sample
def update_sample(adj, sample):
    adj.g = sample.g + get_dist(sample, adj)
    adj.h = get_h(adj)
    adj.parent = sample
    adj.f = adj.g + adj.h
    
# get nearby samples based on centroid position
def get_adj(sample):
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
            samples.append(get_samples(sample.x + i, sample.y + j))
    return samples

# A* search processing
def process(cSpace, start, dest):
    array = [[[] for x in range(AStar.width / AStar.grid)] for y in range(AStar.width / AStar.grid)]
    # map samples to their positions in grid space via their centroid positions
    for i in cSpace:
        cx, cy, angle = centroid_angle(i)
        array[y][x].append(Sample(i, cx, cy, cx / AStar.grid, cy / AStar.grid, angle))
    
    # add end position to samples
    cx, cy, angle = centroid_angle(dest)
    AStar.end = Sample(dest, cx, cy, cx / AStar.grid, cy / AStar.grid, angle)
    array[cy / AStar.grid][cx / AStar.grid].append(AStar.end)
    
    # create start position sample
    cx, cy, angle = centroid_angle(start)
    AStar.start = Sample(start, cx, cy, cx / AStar.grid, cy / AStar.grid, angle)
    AStar.start.h = get_h(AStar.start)
    AStar.start.f = AStar.start.g + AStar.start.f
    
    # start A* search
    heapq.heappush(AStar.op, (AStar.start.f, AStar.start))
    while len(AStar.op):
        # get sample from the open list based on samples f value
        f, sample = heapq.heappop(AStar.op)
        AStar.cl.add(sample)
        # check if it's the final position
        if sample.coords is AStar.end.coords:
            return sample
        # get samples which are near to the current
        adj_samples = get_adj(sample)
        for c in adj_samples:
            if c not in AStar.cl:
                if (c.f, c) in AStar.op:
                    if c.g > (sample.g + get_dist(sample, c)):
                        update_sample(c, sample)
                else:
                    update_sample(c, sample)
                    heapq.heappush(AStar.op, (c.f, c))

def main(inputfile, outputfile):
    global minArea
    global AStar
    global obstacles
    global array
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
    rmin = 7 * (number - 1)
    minArea = np.pi * rmin ** 2
#     for i in range(number):
#         # Create and initialise ASVs
#         asv.append(ASV(i, start[i * 2], start[i * 2 + 1], finish[i * 2], finish[i * 2 + 1]))
#         if i is not 0:
#             asv[i].boom = start[-(number - i)]
    # Extracts how much the obstacles are required to be expanded by 
    expand = obstacle_transform(asv)
    
#    src = cv2.cv.fromarray(grid)
#    cv2.cv.ShowImage('win1', src)
#    cv2.waitKey()

    # Creating obstacles in grid
    for j in range(int(lines[3].strip('\n'))):
        obstacle = remove_decimal(lines[j + 4].strip('\n').split(' '))
        obstacles.append(obstacle)
        final_obstacle = [obstacle[1] + expand[0], obstacle[5] + expand[1] + 1, obstacle[0] + expand[2], obstacle[4] + expand[3] + 1]
        index = 0
        while index < len(final_obstacle):
            if final_obstacle[index] < 0:
                final_obstacle[index] = 0
            index += 1 
        grid[final_obstacle[0]:final_obstacle[1], final_obstacle[2]:final_obstacle[3]] = 1

    process(cSpace)
    display_path(output)
    output.close()
    file.close()

if __name__ == '__main__':
    if(len(sys.argv) is not 3):
        print "Usage: python assg1_42027249_42229904.py desired_input_file desired_output_file"
        sys.exit(1)
    else:
        main(sys.argv[1], sys.argv[2])
    
