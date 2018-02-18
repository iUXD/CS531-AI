## This code is for SuDoKu Agent.
# Authors: Liqiang He, Eugene Seo
from fixed_baseline import *
from MCV import *
from Inference import *
from utility import *



def forward_checking(cells_status):
    for i in range(81):
        if cells_status[i][0] != 0:         # if the cell number is fixed(given), then forward check it
            clean_row(i, cells_status)
            clean_col(i, cells_status)
            clean_box(i, cells_status)

def sudoku(initialState):
    # input:     initialState,a str of 81 initial values
    print(initialState)
    # get data structures
    cells_status = get_initialDict(initialState)
<<<<<<< HEAD
=======
    # forward checking
    forward_checking(cells_status)
    #print_sudoku(cells_status)

    inference(cells_status, 11) # naked_single
    inference(cells_status, 12) # hidden_single
    inference(cells_status, 21) # naked_pairs
    inference(cells_status, 22) # hidden_pairs
    inference(cells_status, 31) # naked_triples
    inference(cells_status, 32) # hidden_triples
    #print_sudoku(cells_status)
>>>>>>> 221e53f136dd63e6e71d33c591b41c0e34589528

    # apply fixed baseline approach
    success, result_cells, used_steps = fixed_baseline(cells_status, 0, 0)
    print(check_goal_3rule(result_cells))
    print(used_steps)
    return ""


if __name__ == '__main__':
    # load data
    filePath = 'data/sudoku-problems.txt'
    samples = getData(filePath)

<<<<<<< HEAD
    test = samples[13][0]
=======
    test = samples[77][0]
>>>>>>> 221e53f136dd63e6e71d33c591b41c0e34589528
    sudoku(test)