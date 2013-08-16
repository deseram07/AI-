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
    return possible
    
        
def sucessor(previous_state_matrix):
    '''
    find the position of the empty slot (0 coordinate) in the 
    current state matrix and apply the actionspace. Function
    returns the world dynamics 
    '''
    current_state = [] 
    previous_state_shape = previous_state_matrix.shape
    req_coord = [0,0]
    for item in previous_state_matrix:
        if req_coord[1] == previous_state_shape[0]-1:
            req_coord[0] += 1
            req_coord[1] = 0
        if item == 0:
            break
        req_coord[1] += 1
    
    possible = actionspace(req_coord)
    
    for coordinate in possible:
        current_state_matrix = np.zeros(previous_state_matrix.shape)
        current_state_matrix = np.copy(previous_state_matrix)
        r,c = coordinate
        to_r, to_c = (req_coord[0]+r, req_coord[1]+c)  #other cell affected due to change
        from_r, from_c = req_coord
        current = [previous_state_matrix[to_r,to_c], previous_state_matrix[from_r, from_c]]
        current_state_matrix[to_r,to_c] = current[1]
        current_state_matrix[from_r, from_c] = current[0]
        current_state.append(current_state_matrix)
        
    print current_state    

def main(input_filename):
    input_file = open(input_filename, 'r')
    var = input_file.readlines()
    startmatrix = np.array(var[0].strip('\n').strip(' ').split(' ')).reshape(3,3)
    finishmatrix = np.array(var[1].strip('\n').strip(' ').split(' ')).reshape(3,3)
    sucessor(startmatrix)
    
    
if __name__ == '__main__':
    main(sys.argv[1])