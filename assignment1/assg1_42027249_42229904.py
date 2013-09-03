import sys
from utility import *

            
# gets distance from one sample configuration to another
def get_dist(sample, other):
    distx = []
    disty = []
    for i in range(len(sample.coords) / 2):
        distx.append(abs(sample.coords[i*2] - other.coords[i*2]))
        disty.append(abs(sample.coords[i*2 + 1] - other.coords[i*2 + 1]))
    distx.sort(reverse=True)
    disty.sort(reverse=True)
    return distx[0] + disty[0]

# converts back to given workspace
def get_decimal(coords):
    points = []
    temp = []
    print coords
    for i in range(len(coords)):
        temp.append(coords[i][0])
        temp.append(coords[i][1])
    for j in temp:
        points.append(float(j)/1000.0)
    return points

# output the path to file
def display_path(outputfile, sample):

    print 'path found'
    path = []
    ccxx = []
    ccyy = []
#     print AStar.start.coords
    # creates path from the end to the start inserting into the beginning 
    while sample.parent is not AStar.start:
        for j in sample.points:
            print j
#            coords = get_decimal(j)

#            path.insert(0, coords)

        sample = sample.parent

    # inserts the start configuration into the path
#    for i in range(len(ccxx)-1):
#        xxx = ccxx[i+1]-ccxx[i]
#        yyy = ccyy[i+1]-ccyy[i]
#        print np.sqrt(xxx**2 + yyy**2)
#    coords = get_decimal(AStar.start.coords)
#    path.insert(0, coords)
#    print path
    # outputs the path with the coordinates of each configuration separated by spaces
    xp = []
    yp = []
    lines = 0
    previous = path[0]
    data = ''
    
    f = 0
    for i in previous:
        f += 1
        data += str(i)
        if f != len(previous):
            data += " "
    lines += 1
    data += "\n"
        
    for x in range(1,len(path)):
#        current = path[x]
#        print path[x]
#        move = interpolate(current, previous)
#        previous = current
#        for i in pa
#        f = 0
#        for coord in move:
#            for i in coord:
#                f += 1
#                data += str(i)
#                if f != len(previous):
#                    data += " "
#            lines += 1
#            data += "\n"
#            f = 0
        if debug:
            for i in range(len(path[x])/2):
                xp.append(1000.0 * path[x][i*2])
                yp.append(1000.0 * path[x][i*2 + 1])
                ox1 = [0,200,200,0,0]
                ox2 = [500,700,700,500,500]
                oy1 = [200,200,400,400,200]
                oy2 = [600,600,900,900, 600]
#            print xp, yp
            py.plot(ox1, oy1, '-+')
            py.plot(ox2, oy2, '-+')
            py.plot(xp, yp, '-+')
            py.show()
            xp = []
            yp = []
    length = str(lines) + ' ' + "0.52\n"
    text = length + data
#    outputfile.write(text)
    
def dist(sample, other):
    distx = abs(sample.coords[0] - other.coords[0])
    disty = abs(sample.coords[1] - other.coords[1])
    return distx+ disty

    
# returns the estimated cost to destination from current position
def get_h(sample):
    h = dist(sample, AStar.end)
#     (abs(sample.cx - AStar.end.cx) + abs(sample.cy - AStar.end.cy)) * 10 + abs(sample.angle - AStar.end.angle) / 10
    return h

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
    x = int(sample.coords[0]/ AStar.grid)
    y = int(sample.coords[1]/ AStar.grid)
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


def points_to_polar(coords, dir):
    polar = [coords[0], coords[1]]
    rotate = angles(Point(coords[0]+1, coords[1]), Point(coords[0],coords[1]), Point(coords[2],coords[3]))
    if dir < 0:
        rotate = 2*np.pi - rotate
    angle = []
    lengths = [boom_length(Point(coords[0],coords[1]),Point(coords[2],coords[3]))]
    for i in range(len(coords)/2-2):
        lengths.append(boom_length(Point(coords[(i+1)*2],coords[(i+1)*2+1]), Point(coords[(i+2)*2], coords[(i+2)*2+1])))
        if dir < 0:
            angle.append(np.pi+angles(Point(coords[i*2], coords[i*2+1]), Point(coords[(i+1)*2],coords[(i+1)*2+1]), Point(coords[(i+2)*2],coords[(i+2)*2+1])))
        else:
            angle.append(np.pi-angles(Point(coords[i*2], coords[i*2+1]), Point(coords[(i+1)*2],coords[(i+1)*2+1]), Point(coords[(i+2)*2],coords[(i+2)*2+1])))
    polar.append(rotate)
    polar.append(lengths)
    polar.append(angle)
    return polar 

# A* search processing
def process(cSpace, start, dest, dir):
    array = [[[] for x in range(AStar.width / AStar.grid)] for y in range(AStar.width / AStar.grid)]
    # map samples to their positions in grid space via their centroid positions
#     print cSpace
    for i in cSpace:
        array[int(i[1]) / AStar.grid][int(i[0]) / AStar.grid].append(Sample(i))
    
    finish = points_to_polar(dest, dir)  
    AStar.end = Sample(finish)
    array[AStar.end.coords[1] / AStar.grid][AStar.end.coords[0] / AStar.grid].append(AStar.end)
    
    # create start position sample
    begin = points_to_polar(start, dir)
    AStar.start = Sample(begin)
    AStar.start.h = get_h(AStar.start)
    AStar.start.f = AStar.start.g + AStar.start.f
    
    # start A* search
    heapq.heappush(AStar.op, (AStar.start.f, AStar.start))
    while len(AStar.op):
        # get sample from the open list based on samples f value
        f, sample = heapq.heappop(AStar.op)
        AStar.cl.add(sample)
        for i in range(len(sample.coords)):
            if sample.coords[i] != AStar.end.coords[i]:
                break
            elif i == len(sample.coords) - 1:
                return sample
        # get samples which are near to the current
        adj_samples = get_adj(array, sample)
        for c in adj_samples:
            for d in c:
                for i in range(2):
                    if int(sample.coords[i]) != int(d.coords[i]):
                ########## INTERPOLATE AND CHECK CONNECTION
#                        print d.coords, sample.coords
#                        print '\n'
                        [steps, g] = extract_points(d.coords, sample.coords, AStar,cSpace)
#                        print g
                        if g != -1:
                            if d not in AStar.cl:
                                if (d.f, d) in AStar.op:
                                    if d.g > (sample.g + g):
                                        update_sample(d, sample, g, steps)
                                else:
                                    update_sample(d, sample, g, steps)
                                    heapq.heappush(AStar.op, (d.f, d))
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
    
#    src = cv2.cv.fromarray(grid)
#    cv2.cv.ShowImage('win1', src)
#    cv2.waitKey()

    # Creating obstacles in grid
    for j in range(int(lines[3].strip('\n'))):
        obstacle = remove_decimal(lines[j + 4].strip('\n').split(' '))
        obstacles.append(obstacle)

    for i in obstacles:
        x = sorted(i[::2])
        y = sorted(i[1::2])
        AStar.obstacle_x.append([x[0],x[-1]]) #[[x_low,x_high],[x1_low,x1_high]]
        AStar.obstacle_y.append([y[0],y[-1]])
    i = 2
    cSpace = obtain_random_points(asv, AStar,5000)
    end = process(cSpace, start[:-number+1], finish[:-number+1], asv[0].direction)
    while end == False:
        print 'trying again'
        cSpace = obtain_random_points(asv, AStar, 1000)
        end = process(cSpace, start[:-number+1], finish[:-number+1], asv[0].direction)
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
    

