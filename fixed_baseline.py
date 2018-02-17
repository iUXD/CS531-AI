from utility import *
from copy import deepcopy
from Inference import *

def fixed_baseline(cells_status1, n):

    # use a fixed order, row-wise and top to bottom
    if goalState(cells_status1):         # check if satisfy with goal
        return True

    if not constraints(cells_status1):
        return False
    print(n)
    if n == 0:
        return False
    forward_checking(cells_status1)
    naked_single(cells_status1)
    # cells_status = deepcopy(cells_status1)
    for i in range(81):
        cells_status = deepcopy(cells_status1)
        if cells_status[i][0] != 0:         # pick an unassigned variable
            continue
        for value in cells_status[i][1]:
            tempList = assignValue2Cell(i, cells_status, value)
            if fixed_baseline(cells_status, n-1):
                return True
            backAssignment(i, cells_status, tempList)
    return False
    pass