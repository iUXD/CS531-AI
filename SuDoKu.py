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

def sudoku(initialState, rule_list):
    # input:     initialState,a str of 81 initial values
    # print(initialState)
    # get data structures
    cells_status = get_initialDict(initialState)
    #inference_recursive(cells_status,50)
    #print(check_goal_3rule(cells_status))

    # apply fixed baseline approach
    success1, result_cells1, used_steps_fb = fixed_baseline(cells_status, 0, 0, rule_list)
    # print(check_goal_3rule(result_cells))
    # print(used_steps_fb)
    #
    # print("Begin MCV:")
    success2, result_cells2, used_steps_mcv = MCV(cells_status, 0 , rule_list)
    # if success:
    #     print(check_goal_3rule(result_cells))
    # print(used_steps_mcv)
    print(success1, used_steps_fb)
    # result_print(result_cells1)
    result_print(result_cells2)
    return used_steps_fb, used_steps_mcv, success1, success2

def series_sudoku(samples):
    res_fb = []
    res_mcv = []
    rule_lists = []
    rule_lists.append([])
    rule_lists.append([11, 12])
    rule_lists.append([11, 12, 21, 22])
    rule_lists.append([11, 12, 21, 22, 31, 32]) # add rule list 1

    m = len(rule_lists)         # number of rule lists
    n = len(samples)            # 71 samples


    res = [[0 for x in range(n)] for y in range(m)]
    for jdx, rule_list in enumerate(rule_lists):
        for i in range(1, 71):
            test = samples[i][0]
            fb, mcv, s1, s2 = sudoku(test, rule_list)
            res_fb.append(fb)
            res_mcv.append(mcv)
            res[jdx][i] = (i, fb, mcv)
            print(i, fb, mcv, mcv < fb, s1, s2)
    print(res)

if __name__ == '__main__':
    # load data
    filePath = 'data/sudoku-problems.txt'
    samples = getData(filePath)

    # test = samples[1][0]
    # test_rule_list = [11, 12, 21, 22, 31, 32]
    # test_rule_list = []
    # print(sudoku(test, test_rule_list))
    # series_sudoku(samples)
    sudoku(samples[2][0], [])