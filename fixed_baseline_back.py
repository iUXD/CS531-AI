from utility import *
from copy import deepcopy
from Inference import *
# useless, I will delete it finally -- liqiang
def fixed_baseline(cells_status, n):
    # use a fixed order, row-wise and top to bottom
    if check_goal_3rule(cells_status):              # check if satisfy with goal
        return True

    if violate_constraints(cells_status):           # check if violate the constraints
        return False

    if n == 0:                                      # check if exhaust the steps
        return False

    temp_cells_status = deepcopy(cells_status)      # make a deep copy

    forward_checking(temp_cells_status)                  # do inference cut
    test_naked_single(temp_cells_status)

    if violate_constraints(temp_cells_status):           # check if satisfy the constraints
        # cells_status = deepcopy(temp_cells_status)  # retrieve the copy
        return False
    if check_goal_3rule(temp_cells_status):
        cells_status = deepcopy(temp_cells_status)
        return True
    if get2lines(temp_cells_status)[:31] == '2483176959615284375739461286157':
        print("------------------------------------------------------------------------------------------")
    for i in range(81):                                 # simple order to select variables
        if temp_cells_status[i][0] != 0:                     # skip the assigned variable
            continue
        # Then DFS

        if helper(i, temp_cells_status, n - 1):                  # if all values cannot assign to this variable i
            cells_status = deepcopy(temp_cells_status)
            if i == 80:
                break
            continue
        # cells_status = deepcopy(temp_cells_status)  # retrieve to previous status
        print("==============================================================================================", i, n)
        return False
        # if not helper(i, cells_status, n):              # if all values cannot assign to this variable i
        #     cells_status = deepcopy(temp_cells_status)  # retrieve to previous status
        #     return False
    cells_status = deepcopy(temp_cells_status)
    print("==================================================", n)
    print_remain(cells_status)
    print("==================================================", n)
    # Then finished all 81 variable assignment
    return True

def helper(i, cells_status, n):
    if len(cells_status[i][1]) == 0:
        return True
    copy_status = deepcopy(cells_status)                    # deep copy of all cells
    value_domain = deepcopy(copy_status[i][1])              # deep copy of this cell's value domain

    for value in value_domain:
        print(n, i, value)
        copy2 = deepcopy(copy_status)
        assignValue2Cell(i, copy2, value)
        if fixed_baseline(copy2, n - 1):
            cells_status = deepcopy(copy2)
            return True
        # cells_status = deepcopy(copy_status)            # failed with this value assignment, have to retrieve
        # backAssignment(i, cells_status, tempList)
    return False


def printSum(cells):
    res = 0
    for i in range(81):
        res += cells[i][0]

    res2 = 0
    for i in range(1, 10):
        res2 += i
    print(res, res2 * 9)
    return res, res2 * 9