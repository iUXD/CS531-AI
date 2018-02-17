## This code is for SuDoKu Agent.
# Authors: Liqiang He, Eugene Seo
from fixed_baseline import *
from MCV import *
MAXNUM = 1000

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
    # forward checking
    forward_checking(cells_status)

    # apply fixed baseline approach
    fixed_baseline(cells_status, MAXNUM)

    # print result
    result_print(cells_status)
    pretty_print(cells_status)
    return ""


if __name__ == '__main__':
    # load data
    filePath = 'data/sudoku-problems.txt'
    samples = getData(filePath)

    test = samples[1][0]
    sudoku(test)

