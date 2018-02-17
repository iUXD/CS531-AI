from utility import *

def fixed_baseline(cells_status):
    # use a fixed order, row-wise and top to bottom
    if goalState(cells_status):
        return True
    pass