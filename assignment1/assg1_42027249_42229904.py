import sys
import numpy as np
import math
from utility import *
import heapq

# Working on grid (1000 x 1000) where obstacles are represented by 1s and clear is represented by 0s

def init_grid(AStar, grid):
    for x in range(AStar.width):
        for y in range(AStar.height):
            if grid[x][y] == 1:
                reachable = False
            else:
                reachable = True
            AStar.cells.append(CELL(x,y,reachable))
            
# Astar search processing
def process(AStar, asv):
    start = get_cell(AStar, asv[0].x, asv[0].y)
    start.h = get_h(asv[0])
    start.f = start.g + start.f
    heapq.heappush(AStar.op, (start.f, start))
    while len(AStar.op):
        f, cell = heapq.heappop(AStar.op)
        

def main(filename):
    global minArea
    AStar = Astar()
    grid = np.zeros(shape=(1000, 1000))
    file = open(filename, 'r')
    lines = file.readlines()
    start = remove_decimal(lines[1].strip('\n').split(' '))
    finish = remove_decimal(lines[2].strip('\n').split(' '))
    asv = []
    number = int(lines[0].strip('\n'))
    rmin = 7 * (number - 1)
    minArea = np.pi * rmin * rmin
    for i in range(number):
        # Create and initialise ASVs
        asv.append(ASV(i, start[i * 2], start[i * 2 + 1], finish[i * 2], finish[i * 2 + 1]))
        if i is not 0:
            asv[i].boom = start[-(number - i)]
            boom_length(asv[i], asv[i-1])

    # Creating obstacles in grid
    for j in range(int(lines[3].strip('\n'))):
        obstacle = remove_decimal(lines[j + 4].strip('\n').split(' '))
        # Iterate through column of position of the obstacle
        for n in range(obstacle[1], obstacle[3]):
            # Iterate through row of position of the obstacle
            for m in range(obstacle[0], obstacle[2]):
                grid[m][n] = 1
    
    init_grid(AStar, grid)
    process(AStar, asv)
    
        


if __name__ == '__main__':
    if(len(sys.argv) is not 2):
        print "Usage: python assg1_42027249_42229904.py desired_input_file"
        sys.exit(1)
    else:
        main(sys.argv[1])
    
