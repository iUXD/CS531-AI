from utility import *
from copy import deepcopy
from Inference import *
MAXNUM = 500
def fixed_baseline(cells_status, n, idx, rule_list):
    # use a fixed order, row-wise and top to bottom
    # idx is the index in the 81 variables

    if idx == 81:                                       # checked all variables
        return check_goal_3rule(cells_status), cells_status, n

    if check_goal_3rule(cells_status):                  # check if satisfy with goal
        return True, cells_status, n

    if violate_constraints(cells_status):               # check if violate the constraints
        return False, None, n

    if n > MAXNUM:                                          # check if exhaust the steps
        return False, None, n

    forward_checking(cells_status)                      # do inference cut
    # test_naked_single(cells_status)
    # inference_recursive(cells_status, rule_list, MAXNUM)
    if violate_constraints(cells_status):               # check if satisfy the constraints
        # if cells_status != None:
        #     result_print(cells_status)
        #     # pretty_print(cells_status)
        #     checkZeros(cells_status)
        #     exit(0)
        # print("===========err")

        return False, None, n
    if check_goal_3rule(cells_status):
        return True, deepcopy(cells_status), n

    while idx < 80 and cells_status[idx][0] != 0:       # pick one unassigned variable
        idx += 1

    if idx == 80:
        if cells_status[idx][1] != []:
            pass
        else:
            if check_goal_3rule(cells_status):
                return True, deepcopy(cells_status), n
            return False, None, n


    value_domain = cells_status[idx][1]                 # get this cell's value domain
    for value in value_domain:
        copy2 = deepcopy(cells_status)                  # use a deep copy, since each value assignment will change
                                                        # the whole 81 variables and domains
        assignValue2Cell(idx, copy2, value)             # assignment value to variable
        success, result_Cells, steps = fixed_baseline(copy2, n + 1, idx + 1, rule_list)       # BT to next nodes
        if success:
            cells_status = deepcopy(result_Cells)
            return True, deepcopy(result_Cells), steps
    return False, None, n

def checkZeros(cells):
    for i in range(81):
        if cells[i][0] == 0 and len(cells[i][1]) == 0:
            print (i,cells[i])