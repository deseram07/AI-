import sys
from utility import *

            
# gets distance from one sample configuration to another
def get_dist(sample, other):
    distx = []
    disty = []
    for i in range(len(sample.coords) / 2):
        distx.append(abs(sample.coords[i * 2] - other.coords[i * 2]))
        disty.append(abs(sample.coords[i * 2 + 1] - other.coords[i * 2 + 1]))
    distx.sort(reverse=True)
    disty.sort(reverse=True)
    return distx[0] + disty[0]

# converts back to given workspace
def get_decimal(coords):
    points = []
    temp = []
    for i in range(len(coords)):
        temp.append(coords[i][0])
        temp.append(coords[i][1])
    for j in temp:
        points.append(float(j) / 1000.0)
    return points

# output the path to file
def display_path(outputfile, sample, init_coord):

    print 'path found'
    path = []
    some = []
    data = ''
    lines = 0
#     print AStar.start.coords
    # creates path from the end to the start inserting into the beginning 
    while sample.parent is not None:
        for j in sample.points:
            lines += 1
            coords = get_decimal(j)
            print coords
            some.append(coords)
        path.insert(0, some)
        some = []
        sample = sample.parent
        
    prev = init_coord
    for i in path:
        for j in i:
            for point in j:
                point = round(point, 3)
    
                data += str(point)
                data += ' '
            data += '\n'
    length = str(lines) + ' ' + str(float(lines) / 1000) + "\n"
    text = length + data
    outputfile.write(text)
    
def dist(sample, other):
    distx = abs(sample.coords[0] - other.coords[0])
    disty = abs(sample.coords[1] - other.coords[1])
    return distx + disty

    
# returns the estimated cost to destination from current position
def get_h(sample):
    h = dist(sample, AStar.end)
#     (abs(sample.cx - AStar.end.cx) + abs(sample.cy - AStar.end.cy)) * 10 + abs(sample.angle - AStar.end.angle) / 10
    return h * 200

# returns samples from a given location
def get_samples(array, x, y):
    return array[int(y)][int(x)]

# updates adjacent sample with details from current sample
def update_sample(adj, sample, g, steps):
    adj.g = sample.g + g
    adj.h = get_h(adj)
    adj.parent = sample
    adj.points = steps
    adj.f = adj.g + adj.h
    
# get nearby samples based on centroid position
def get_adj(array, sample):
    samples = []
    movex = [0]
    movey = [0]
    x = int(sample.coords[0] / AStar.grid)
    y = int(sample.coords[1] / AStar.grid)
    # checks where to get samples from
    if x < ((AStar.width / AStar.grid) - 1):
        movex.append(1)
    if y > 0:
        movey.append(-1)
    if x > 0:
        movex.append(-1)
    if y < ((AStar.width / AStar.grid) - 1):
        movey.append(1)
    # gets samples from available grid squares
    for i in movex:
        for j in movey:
            samples.append(get_samples(array, x + i, y + j))

    return samples

def points_to_polar(coords):
    polar = [float(coords[0]), float(coords[1])]
    rotate = angles(Point(coords[0]+1, coords[1]), Point(coords[0],coords[1]), Point(coords[2],coords[3]))
    if coords[1] > coords[3]:
        rotate = 2*np.pi - rotate
    angle = []
    lengths = [boom_length(Point(coords[0],coords[1]),Point(coords[2],coords[3]))]
    for i in range(len(coords)/2-2):
        lengths.append(boom_length(Point(coords[(i+1)*2],coords[(i+1)*2+1]), Point(coords[(i+2)*2], coords[(i+2)*2+1])))
        temp = angles(Point(coords[(i+1)*2]+1,coords[(i+1)*2+1]),Point(coords[(i+1)*2],coords[(i+1)*2+1]), Point(coords[(i+2)*2],coords[(i+2)*2+1]))
        if coords[(i+1)*2+1] > coords[(i+2)*2+1]:
            temp = 2*np.pi - temp
        temp = temp - rotate
        if temp < 0:
            temp = 2*np.pi + temp
        angle.append(temp)
    polar.append(rotate)
    polar.append(lengths)
    polar.append(angle)
    return polar 

# A* search processing
def process(cSpace, start, dest):
    array = [[[] for x in range(AStar.width / AStar.grid)] for y in range(AStar.width / AStar.grid)]
    # map samples to their positions in grid space via their centroid positions
#     print cSpace
    for i in cSpace:
        array[int(i[1]) / AStar.grid][int(i[0]) / AStar.grid].append(Sample(i))
    

    finish = points_to_polar(dest)  
    AStar.end = Sample(finish)
    array[int(AStar.end.coords[1]) / AStar.grid][int(AStar.end.coords[0]) / AStar.grid].append(AStar.end)
    
    # create start position sample
    begin = points_to_polar(start)
    AStar.start = Sample(begin)
    AStar.start.h = get_h(AStar.start)
    AStar.start.f = AStar.start.g + AStar.start.f
    
    # start A* search
    heapq.heappush(AStar.op, (AStar.start.f, AStar.start))
    m = 0
    while len(AStar.op):
        # get sample from the open list based on samples f value
        f, sample = heapq.heappop(AStar.op)
#        if m == 2:
#            sys.exit()
#        m += 1
        AStar.cl.add(sample)
        for i in range(len(sample.coords)):
            if sample.coords[i] != AStar.end.coords[i]:
                break
            elif i == len(sample.coords) - 1:
                return sample
        # get samples which are near to the current
#        print sample.coords
        adj_samples = get_adj(array, sample)
        
        for c in adj_samples:
            for d in c:
#                print '1'
#                print sample.coords
                if int(sample.coords[0]) != int(d.coords[0]) and int(sample.coords[1]) != int(d.coords[1]):
            ########## INTERPOLATE AND CHECK CONNECTION
#                    print'2'
#                    print sample.coords
#                    print d.coords, sample.coords
                    [steps, g] = extract_points(d.coords, sample.coords, AStar, cSpace)
#                    print '3'
#                    print sample.coords
                    if g != -1:
                        if d not in AStar.cl:
                            if (d.f, d) in AStar.op:
                                if d.g > (sample.g + g):
                                    update_sample(d, sample, g, steps)
                            else:
                                update_sample(d, sample, g, steps)
                                heapq.heappush(AStar.op, (d.f, d))
#                            print '4'
#                            print sample.coords
    return False             
        

def main(inputfile, outputfile):
    global minArea
    global AStar
    obstacles = []
    cSpace = []
    obstacle_x = []
    obstacle_y = []
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
    
    # Creating obstacles in grid
    for j in range(int(lines[3].strip('\n'))):
        obstacle = remove_decimal(lines[j + 4].strip('\n').split(' '))
        obstacles.append(obstacle)

    for i in obstacles:
        x = sorted(i[::2])
        y = sorted(i[1::2])
        AStar.obstacle_x.append([x[0], x[-1]])  # [[x_low,x_high],[x1_low,x1_high]]
        AStar.obstacle_y.append([y[0], y[-1]])
    i = 2
    cSpace = obtain_random_points(asv, AStar, 500)
    end = process(cSpace, start[:-number + 1], finish[:-number + 1])
    while end == False:
        print 'trying again'
        cSpace = obtain_random_points(asv, AStar, 1000)
        end = process(cSpace, start[:-number + 1], finish[:-number + 1])
        i += 1
    display_path(output, end, start)
    output.close()
    file.close()

if __name__ == '__main__':
    if(len(sys.argv) is not 3):
        print "Usage: python assg1_42027249_42229904.py desired_input_file desired_output_file"
        sys.exit(1)
    else:
        main(sys.argv[1], sys.argv[2])
    

