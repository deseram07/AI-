import math
import numpy as np


def ccw(A, B, C):
    """
    Returns true if it rotates about B
    """
    ax,ay = B[0]-A[0],B[1]-A[1]
    bx,by = B[0]-C[0],B[1]-C[1]
    return ((ax*by) - (ay*bx))
#    return (C[1] - A[1]) * (B[0] - A[0]) - (B[1] - A[1]) * (C[0] - A[0])

def length(start, end):
    """
    Finds the vector start -> end
    """
    boom = math.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)
    return boom

def angle_about_mid(start, middle, end):
    """
    Finds the angle between 3 points about mid
    """
    a = length(middle, end)
    b = length(start, middle)
    c = length(start, end)
    frac = (a ** 2.0 + b ** 2.0 - c ** 2.0) / (2.0 * a * b)
    if frac > 1:
        frac = 1
    elif frac < -1:
        frac = -1
#    print ((a ** 2.0 + b ** 2.0 - c ** 2.0) / (2.0 * a * b))
    angle = (np.arccos(frac))
#    print angle
#    if angle == 'nan':
#        return angle
#    else:
#        return np.pi
    return angle

# Return true if line segments AB and CD intersect
def intersect(A, B, C, D):
    return np.sign(ccw(A, C, D)) != np.sign(ccw(B, C, D)) and np.sign(ccw(A, B, C)) != np.sign(ccw(A, B, D))


# Check for obstacle between point1 and point2 returns True for a collision
def check_collision(person, point1, point2):
    A = point1[:]
    B = point2[:]
    for i in person.obstacles: # [[[minx, miny], [maxx, maxy]],[....]]
        # corners = [[minx,miny], [minx,maxy], [maxx,miny], [maxx,maxy]]
        corners = [i[0], [i[0][0], i[1][1]], [i[1][0], i[0][1]], i[1]]
        for j in range(len(corners)-1):
            C = corners[j]
            if j == len(corners):
                D = corners[0]
            else:
                D = corners[j+1]
            if intersect(A, B, C, D):
                return True
    return False

# normalise angle to 0->360 degrees
def norm_ang(angle):
    if angle < 0:
        angle = 360 + angle
    elif angle > 360:
        angle = angle - 360
    return angle