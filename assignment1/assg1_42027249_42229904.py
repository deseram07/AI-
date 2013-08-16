import sys
import numpy as np
import math


# working on grid (1000 x 1000) where obstacles are represented by 1s and clear is represented by 0s

# creating an ASV
class ASV:
    def __init__(self, num, x, y):
        self.num = num
        self.x = x
        self.y = y
        self.previous = None
        self.boom = 0


# for printing the list of ASVs    
def print_asv(asv):
    for i in range(len(asv)):
        print str(asv[i].num)+', '+str(asv[i].x)+', '+str(asv[i].y)+', '+str(asv[i].previous)


# takes a list of string decimals and converts to a number and returns list of ints
def remove_decimal(list):
    for i in range(len(list)):
        list[i] = int(float(list[i])*1000)
        
    return list

# calculates the distance between two points
def boom_length(start, end):
    boom = math.sqrt((start.x-end.x)**2+(start.y-end.y)**2)
    return boom


# calculates angle between 3 ASVs
def angles(start, middle, end):
    a = boom_length(middle, end)
    b = boom_length(start, middle)
    c = boom_length(start, end)
    angle = math.degrees(math.acos((a**2+b**2-c**2)/(2*a*b)))
    print angle


def main(filename):
    global minArea
    grid = np.zeros(shape=(1000,1000))
    file = open(filename, 'r')
    lines = file.readlines()
    start = remove_decimal(lines[1].strip('\n').split(' '))
    finish = remove_decimal(lines[2].strip('\n').split(' '))
    asv = []
    number = int(lines[0].strip('\n'))
    rmin = 7*(number-1)
    minArea = np.pi*rmin*rmin
    for i in range(number):
        # create and initialise ASVs
        asv.append(ASV(i, start[i*2], start[i*2+1]))
        if i is not 0:
            asv[i].previous = asv[i-1]
            asv[i].boom = start[-(number-i)]
            print asv[i].boom
            boom_length(asv[i], asv[i].previous)
        
    angles(asv[0], asv[1], asv[2])
    print_asv(asv)
    # Creating obstacles in grid
    for j in range(int(lines[3].strip('\n'))):
        obstacle = remove_decimal(lines[j+4].strip('\n').split(' '))
        # iterate through column of position of the obstacle
        for n in range(obstacle[1],obstacle[3]):
            # iterate through row of position of the obstacle
            for m in range(obstacle[0],obstacle[2]):
                grid[m][n] = 1
    
#     print grid
        


if __name__ == '__main__':
    if(len(sys.argv) is not 2):
        print "Usage: python assg1_42027249_42229904.py desired_input_file"
        sys.exit(1)
    else:
        main(sys.argv[1])
    