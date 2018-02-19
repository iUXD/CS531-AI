from heapq import heapify, heappop, heappush
from utility import *
from copy import deepcopy
from Inference import *

MAXNUM = 500
def MCV(cells_status, n, rule_list):
    # print("----------------------0", n)

    # Most Constrained Variable, used a heap
    if check_goal_3rule(cells_status):                  # check if satisfy with goal
        return True, cells_status, n

    if violate_constraints(cells_status):               # check if violate the constraints
        return False, None, n

    if n > MAXNUM:                                      # check if exhaust the steps
        return False, None, n

    # forward_checking(cells_status)                      # do inference cut
    # test_naked_single(cells_status)
    inference_recursive(cells_status, rule_list, MAXNUM)

    if violate_constraints(cells_status):               # check if satisfy the constraints
        return False, None, n

    if check_goal_3rule(cells_status):                  # check if satisfy with goal
        return True, deepcopy(cells_status), n

    pq = get_heap(cells_status)                         # put candidates in a queue

    if len(pq) == 0:
        return False, None, n
    _, idx = heappop(pq)

    value_domain = cells_status[idx][1]                 # get this cell's value domain

    for value in value_domain:
        copy2 = deepcopy(cells_status)                  # use a deep copy, since each value assignment will change
                                                        # the whole 81 variables and domains
        assignValue2Cell(idx, copy2, value)             # assignment value to variable
        success, result_Cells, steps = MCV(copy2, n + 1, rule_list)    # BT to next nodes
        if success:
            cells_status = deepcopy(result_Cells)
            return True, cells_status, steps

    return False, None, n



def get_heap(cells_status):
    pq = []  # heap
    heapify(pq)
    for i in range(81):
        if len(cells_status[i][1]) != 0:
            heappush(pq, (len(cells_status[i][1]), i))
    return pq
