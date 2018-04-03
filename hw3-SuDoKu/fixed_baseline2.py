from utility import *
from copy import deepcopy
from Inference import *
# useless, I will delete it finally -- liqiang
def fixed_baseline(cells_status, n, idx):
    # use a fixed order, row-wise and top to bottom
    # idx is the index in the 81 variables
    if idx == 81:                                       # checked all variables
        return check_goal_3rule(cells_status)

    if check_goal_3rule(cells_status):                  # check if satisfy with goal
        return True, cells_status

    if violate_constraints(cells_status):               # check if violate the constraints
        return False, None

    if n == 0:                                          # check if exhaust the steps
        return False, None

    temp_cells_status = deepcopy(cells_status)          # make a deep copy

    forward_checking(temp_cells_status)                 # do inference cut
    test_naked_single(temp_cells_status)

    if violate_constraints(temp_cells_status):          # check if satisfy the constraints
        return False, None
    if check_goal_3rule(temp_cells_status):
        cells_status = deepcopy(temp_cells_status)
        return True, cells_status

    while idx < 80 and temp_cells_status[idx][0] != 0:       # pick one unassigned variable
        idx += 1

    if idx == 80:
        if check_goal_3rule(temp_cells_status):

            cells_status = deepcopy(temp_cells_status)
            return True, cells_status
        return False, None

    value_domain = deepcopy(temp_cells_status[idx][1])  # deep copy of this cell's value domain
    for value in value_domain:
        copy2 = deepcopy(temp_cells_status)
        assignValue2Cell(idx, copy2, value)
        res, backCells = fixed_baseline(copy2, n - 1, idx + 1)

        if res:
            cells_status = deepcopy(backCells)
            return True, cells_status
    return False, None



def test(arr):

    arr[0] = 1
    return True


def printSum(cells):
    res = 0
    for i in range(81):
        res += cells[i][0]

    res2 = 0
    for i in range(1, 10):
        res2 += i
    print(res, res2 * 9)
    return res, res2 * 9