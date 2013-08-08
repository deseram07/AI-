#http://www.laurentluce.com/posts/solving-mazes-using-python-simple-recursivity-and-a-search/

import sys

if len(sys.argv) != 4:
    print 'usage: python shortpath.py start end'
    sys.exit(1)
    
filename = sys.argv[1]
global start, goal
start = sys.argv[2]
goal = sys.argv[3]

class Place(object):
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

def display_path(place):
    print 'path: '
    path = []
    while place is not start:
        path.insert(0, place.name)
        place = place.parent
    #path.reverse()
    print start.name+ ', ' + ', '.join(path)
    
    
f = open(filename, 'r')
i = -1
count = 0
flag = 0
names = []
connect= [] 
for line in f:
    if i == -1:
        count = int(line)
    elif ((i == count)&(flag==0)):
        count = int(line)
        i = -1
        flag = 1
    else:
        if(flag==0):
            names.append(line.rstrip('\n'))
        else:
            words = (line.rstrip('\n')).split()
            connect.append(words)
    i += 1

closedSet = set()
openSet = set()
openList = []
closedList = []
stepScore = 10
steps = 0
start = Place(start)
start.g = 0
start.h = 70
start.f = start.g + start.h
openSet.add(start)
openList.append(start.name)
while openSet:
    element = openSet.pop()
    closedSet.add(element)
    print openList
    print element.name
    openList.remove(element.name)
    closedList.append(element.name)
    if element.name == goal:
        #finished -- found path---------------------------------------------------------
        print 'path found'
        display_path(element)
        sys.exit(0)
    else:
        result = filter(lambda x:x[0]==element.name, connect)
        result2 = filter(lambda x:x[1]==element.name, connect)
        #print result
        #print result2
        for line in result:
            place = Place(line[1])
            if place.name not in closedList:
                if place.name not in openList:
                    print place.name
                    openSet.add(place)
                    openList.append(place.name)
                    place.g = int(line[2]) + int(element.g)
                    place.h = element.h - 1
                    place.parent = element
                    place.f = place.g + place.h
                    
        for line in result2:
            place = Place(line[0])
            if place.name not in closedList:
                if place.name not in openList:
                    print place.name
                    openSet.add(place)
                    openList.append(place.name)
                    place.g = int(line[2]) + int(element.g)
                    place.h = element.h - 1
                    place.parent = element
                    place.f = place.g + place.h                    
        
    
print 'no path'






