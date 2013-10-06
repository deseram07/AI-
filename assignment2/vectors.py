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
#    print ((a ** 2.0 + b ** 2.0 - c ** 2.0) / (2.0 * a * b))
    angle = (np.arccos((a ** 2.0 + b ** 2.0 - c ** 2.0) / (2.0 * a * b)))
#    print angle
#    if angle == 'nan':
#        return angle
#    else:
#        return np.pi
    return angle