import sys
#import numpy as np
#import math
from utility import *
import heapq
#import cv2

# Working on grid (1000 x 1000) where obstacles are represented by 1s and clear is represented by 0s

def init_grid(grid):
    for x in range(AStar.width):
        for y in range(AStar.height):
            if grid[y][x] == 1:
                reachable = False
            else:
                reachable = True
            AStar.cells.append(Cell(x, y, reachable))
            
def display_path(outputfile):
    print 'path found'
    cell = AStar.end
    while cell.parent is not AStar.start:
        cell = cell.parent
        outputfile.write('%.3f, %.3f\n' % (float(cell.x) / 1000, float(cell.y) / 1000.0))
#        print '%d, %d' % (cell.x, cell.y)
        
# returns the estimated cost to destination from current position
def get_h(cell):
    dist = abs(cell.x - AStar.end.x) + abs(cell.y - AStar.end.y)
    return dist

def get_cell(x, y):
    return AStar.cells[x * AStar.height + y]

def update_cell(adj, cell):
    adj.g = cell.g + 1
    adj.h = get_h(adj)
    adj.parent = cell
    adj.f = adj.g + adj.h
    
def get_adj(cell):
    cells = []
    if cell.x < AStar.width - 1:
        cells.append(get_cell(cell.x + 1, cell.y))
    if cell.y > 0:
        cells.append(get_cell(cell.x, cell.y - 1))
    if cell.x > 0:
        cells.append(get_cell(cell.x - 1, cell.y))
    if cell.y < AStar.height - 1:
        cells.append(get_cell(cell.x, cell.y + 1))
    return cells

# Astar search processing
def process(asv):
    AStar.end = get_cell(asv[0].destx, asv[0].desty)
    AStar.start = get_cell(asv[0].x, asv[0].y)
    AStar.start.h = get_h(asv[0])
    AStar.start.f = AStar.start.g + AStar.start.f
    heapq.heappush(AStar.op, (AStar.start.f, AStar.start))
    while len(AStar.op):
        f, cell = heapq.heappop(AStar.op)
        AStar.cl.add(cell)
        if cell is AStar.end:
            return cell
        adj_cells = get_adj(cell)
        for c in adj_cells:
            if c.reachable and c not in AStar.cl:
                if (c.f, c) in AStar.op:
                    if c.g > cell.g + 1:
                        update_cell(c, cell)
                else:
                    update_cell(c, cell)
                    heapq.heappush(AStar.op, (c.f, c))
            
        

def main(inputfile, outputfile):
    global minArea
    global AStar
    global obstacles
    obstacles = []
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
    minArea = np.pi * rmin * rmin
    for i in range(number):
        # Create and initialise ASVs
        asv.append(ASV(i, start[i * 2], start[i * 2 + 1], finish[i * 2], finish[i * 2 + 1]))
        if i is not 0:
            asv[i].boom = start[-(number - i)]
    asv[0].direction = ccw(asv[0], asv[1], asv[2])
    print asv[0].direction
    # Extracts how much the obstacles are required to be expanded by 
    expand = obstacle_transform(asv)
    
#    src = cv2.cv.fromarray(grid)
#    cv2.cv.ShowImage('win1', src)
#    cv2.waitKey()

    # Creating obstacles in grid
#    for j in range(int(lines[3].strip('\n'))):
#        obstacle = remove_decimal(lines[j + 4].strip('\n').split(' '))
#        obstacles.append(obstacle)
#        final_obstacle = [obstacle[1] + expand[0], obstacle[5] + expand[1] + 1, obstacle[0] + expand[2], obstacle[4] + expand[3] + 1]
#        index = 0
#        while index < len(final_obstacle):
#            if final_obstacle[index] < 0:
#                final_obstacle[index] = 0
#            index += 1 
#        
#        grid[final_obstacle[0]:final_obstacle[1], final_obstacle[2]:final_obstacle[3]] = 1

#    init_grid(grid)
#    process(asv)
#    display_path(output)
    output.close()
    file.close()

if __name__ == '__main__':
    if(len(sys.argv) is not 3):
        print "Usage: python assg1_42027249_42229904.py desired_input_file desired_output_file"
        sys.exit(1)
    else:
        main(sys.argv[1], sys.argv[2])
    

