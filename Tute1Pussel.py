import numpy as np
import sys

def actionspace(Coordinates):
    """
    Gets the current coordinates of the blank spot and 
    returns the action space of for that space
    """
    (row, column) = Coordinates
    possible = [(-1,0), (1,0), (0,-1), (0,1)]
    if row == 0:
        # Cannot go up
        possible.remove((-1,0))
    elif row == 2:
#        cannot go down
        possible.remove((1,0))
    if column == 0:
#        cannot go left
        possible.remove((0,-1))
    elif column == 2:
#        cannot go right
        possible.remove((0,1))
#    return possible
    print possible
    
        
def sucessor(current_state, actionspace):
    '''
    find the position of the empty time (0 coordinate) in the 
    current state matrix and apply the actionspace. Function
    returns the world dynamics 
    '''
    
    

def main(input_filename):
    input_file = open(input_filename, 'r')
    var = input_file.readlines()
    startmatrix = np.array(var[0].strip('\n').strip(' ').split(' ')).reshape(3,3)
    finishmatrix = np.array(var[1].strip('\n').strip(' ').split(' ')).reshape(3,3)
    
    
    
if __name__ == '__main__':
    main(sys.argv[1])