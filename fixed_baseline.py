from utility import *

def fixed_baseline(cells_status, n):
    # use a fixed order, row-wise and top to bottom
    if goalState(cells_status):         # check if satisfy with goal
        return True
    if constraints(cells_status):
        return False
    if n == 0:
        return False
    n -= 1

    inference(cells_status)
    for i in range(81):
        if cells_status[i][0] != 0:         # pick an unassigned variable
            continue
        for value in cells_status[i][1]:
            tempList = assignValue2Cell(i, cells_status, value)
            if fixed_baseline(cells_status):
               return True
            backAssignment(i, cells_status, tempList)
    return False
    pass