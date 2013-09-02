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
    for i in range(len(coords)):
        points.append(float(coords[i]) / 1000.0)
    return points

# output the path to file
def display_path(outputfile, sample):

#     print 'path found'
    path = []
    ccxx = []
    ccyy = []
#     print AStar.start.coords
    # creates path from the end to the start inserting into the beginning 
    while sample.parent is not AStar.start:
        coords = get_decimal(sample.coords)
        path.insert(0, coords)
        ccxx.append(sample.cx)
        ccyy.append(sample.cy)
        sample = sample.parent
    # inserts the start configuration into the path
    for i in range(len(ccxx)-1):
        xxx = ccxx[i+1]-ccxx[i]
        yyy = ccyy[i+1]-ccyy[i]
        print np.sqrt(xxx**2 + yyy**2)
    coords = get_decimal(AStar.start.coords)
    path.insert(0, coords)
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
        current = path[x]
        move = interpolate(current, previous)
        previous = current
        f = 0
        for coord in move:
            for i in coord:
                f += 1
                data += str(i)
                if f != len(previous):
                    data += " "
            lines += 1
            data += "\n"
            f = 0
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
    outputfile.write(text)
        
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
    print "dest = ",cx,cy, "\n", dest
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
        # get sample from the open list based on samples f value
        f, sample = heapq.heappop(AStar.op)
        AStar.cl.add(sample)
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
#                check whether line between corresponding leader asv go through
#                obstacle

#                generate states between them
#                    changing angle and moving
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
    cSpace = obtain_random_points(asv, 1000, obstacles, grid )
    end = process(cSpace, start[:-number+1], finish[:-number+1])
    while end == False:
        print 'trying again'
        cSpace = obtain_random_points(asv, 1000*i, obstacles, AStar)
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
    

