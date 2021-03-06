def getData(filePath):
    with open(filePath, 'r') as f:
        data = f.readlines()
        res = {}
        i = 0
        str = ""
        key = ""
        for line in data:
            line = line.replace("\n","")
            line = line.replace("\t", "")
            line = line.replace(" ", "")
            if len(line.strip()) == 0:
                continue
            if(line.isdigit()):
                str += line
            else:
                if i > 0:
                    res[i] = (str,key,len(str))
                key = line
                str = ""
                i += 1
        res[i] = (str, key, len(str))
            # print(line)
    return res

def get_initialDict(inputStr):
    # return a dictionary, contains 81 keys, value is list
    # if the cell i has value:
    #       res[i] = [value]
    # else:
    #       res[i] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    res = {}
    for i in range(81):
        if inputStr[i] == '0':
            res[i] = [0, [j for j in range(1, 10)]]
        else:
            res[i] = [int(inputStr[i]), []]
    return res

def forward_checking(cells_status):
    for i in range(81):
        if cells_status[i][0] != 0:         # if the cell number is fixed(given), then forward check it
            clean_row(i, cells_status)
            clean_col(i, cells_status)
            clean_box(i, cells_status)

def clean_row(i, cells_status):
    val = cells_status[i][0]
    for idx in row_cells(i):
        remove_candidate(idx, val, cells_status)
    pass

def clean_col(i, cells_status):
    val = cells_status[i][0]
    for idx in col_cells(i):
        remove_candidate(idx, val, cells_status)
    pass

def clean_box(i, cells_status):
    val = cells_status[i][0]
    for idx in box_cells(i):
        remove_candidate(idx, val, cells_status)
    pass

def remove_candidate(i, j, cells_status):
    # remove j from ith key
    if j in cells_status[i][1] and len(cells_status[i][1]) != 0:
        cells_status[i][1].remove(j)

def row_cells(i):
    # return all other row elements
    rowNum = i // 9
    return [j for j in range(rowNum*9, rowNum*9 + 9, 1) if j is not i]

def col_cells(i):
    # return all other col elements
    colNum = i % 9
    return [j * 9 + colNum for j in range(9) if j * 9 + colNum is not i]

def box_cells(k):
    # return all other square elements
    res = []
    if k in [i for j in (range(0, 3), range(9, 12), range(18, 21)) for i in j]:
        res = [i for j in (range(0, 3), range(9, 12), range(18, 21)) for i in j if i is not k]
    elif k in [i for j in (range(3, 6), range(12, 15), range(21, 24)) for i in j]:
        res = [i for j in (range(3, 6), range(12, 15), range(21, 24)) for i in j if i is not k]
    # square 3
    elif k in [i for j in (range(6, 9), range(15, 18), range(24, 27)) for i in j]:
        res = [i for j in (range(6, 9), range(15, 18), range(24, 27)) for i in j if i is not k]
    # square 4
    elif k in [i for j in (range(27, 30), range(36, 39), range(45, 48)) for i in j]:
        res = [i for j in (range(27, 30), range(36, 39), range(45, 48)) for i in j if i is not k]
    # square 5
    elif k in [i for j in (range(30, 33), range(39, 42), range(48, 51)) for i in j]:
        res = [i for j in (range(30, 33), range(39, 42), range(48, 51)) for i in j if i is not k]
    # square 6
    elif k in [i for j in (range(33, 36), range(42, 45), range(51, 54)) for i in j]:
        res = [i for j in (range(33, 36), range(42, 45), range(51, 54)) for i in j if i is not k]
    # square 7
    elif k in [i for j in (range(54, 57), range(63, 66), range(72, 75)) for i in j]:
        res = [i for j in (range(54, 57), range(63, 66), range(72, 75)) for i in j if i is not k]
    # square 8
    elif k in [i for j in (range(57, 60), range(66, 69), range(75, 78)) for i in j]:
        res = [i for j in (range(57, 60), range(66, 69), range(75, 78)) for i in j if i is not k]
    # square 9
    elif k in [i for j in (range(60, 63), range(69, 72), range(78, 81)) for i in j]:
        res = [i for j in (range(60, 63), range(69, 72), range(78, 81)) for i in j if i is not k]
    # print(res)
    return res

def pretty_print(cells_status):
    for key in cells_status:
        print(key, cells_status[key][0], cells_status[key][1])

def result_print(cells_status):
    res = ""
    for i in range(81):
        if i != 0 and i %9 == 0:
            res += '\n'
        if len(cells_status[i][1]) == 0:
            res += str(cells_status[i][0]) + " "
        else:
            res += '0' + " "
    print(res)

def goalState(cells_status):
    # check if current cells are in goal state, if one cell is 0, or its value poll is not empty, return false
    for i in range(81):
        if cells_status[i][0] == 0 or len(cells_status[i][1]) != 0:
            return False
    return True


def violate_constraints(cells_status):
    # if violate constraints, return True
    for i in range(81):
        if cells_status[i][0] == 0 and len(cells_status[i][1]) == 0:        # 0[]
            return True
        if cells_status[i][0] != 0:
            if not rule1(i, cells_status):
                return True
            if not rule2(i, cells_status):
                return True
            if not rule3(i, cells_status):
                return True
    return False

def constraints(cells_status):
    # check if satisfy with all the constraints
    # if there are cells that have not be assigned, but value domain is empty,  return false
    # have to match with three rules, no repeat
    for i in range(81):
        if cells_status[i][0] == 0 and cells_status[i][1] == []:
            # print("=====>", i, cells_status[i])
            return False
        if cells_status[i][0] != 0:
            if not rule1(i, cells_status):
                return False
            if not rule2(i, cells_status):
                return False
            if not rule3(i, cells_status):
                return False
    return True         # means all variable satisfy the constraints
    pass

def assignValue2Cell(i, cells_status, value):
    # assign value to cell i, return the old list
    res = cells_status[i][1]
    cells_status[i][0] = value
    cells_status[i][1] = []
    return res

def backAssignment(i, cells_status, oldList):
    # assign a list to cell i's candidate pool
    cells_status[i][0] = 0
    cells_status[i][1] = oldList
    pass

# print result
def print_sudoku(cells_status):
    result_print(cells_status)
    pretty_print(cells_status)

def test_naked_single(cells_status):
    for i in range(81):
        if cells_status[i][0] == 0 and len(cells_status[i][1]) == 1:
            cells_status[i][0] = cells_status[i][1][0]
            cells_status[i][1] = []

def check_goal_3rule(cells_status):
    for i in range(81):
        if cells_status[i][0] == 0:
            # print(cells_status[i])
            return False
        if not match_3rule(i, cells_status):
            # print(i, cells_status[i])
            return False
    return True

def match_3rule(i, cells_status):
    return rule1(i, cells_status) and rule2(i, cells_status) and rule3(i, cells_status)



def rule1(i, cells_status):
    # check the same row
    for colIdx in row_cells(i):
        if cells_status[colIdx][0] == cells_status[i][0]:
            return False
    return True

def rule2(i, cells_status):
    # check the same colum
    for colIdx in col_cells(i):
        if cells_status[colIdx][0] == cells_status[i][0]:
            return False
    return True

def rule3(i, cells_status):
    # check the same cubic 3X3
    for colIdx in box_cells(i):
        if cells_status[colIdx][0] == cells_status[i][0]:
            return False
    return True
def get2lines(cells_status):
    # print first line
    res = ""
    for i in range(81):
        res += str(cells_status[i][0])
    return  res

def print_remain(cells_status):
    for i in range(81):
        if cells_status[i][1] != []:
            print(i, cells_status[i])


def filled_in_num(cells_status):
    res = 0
    for i in range(81):
        if cells_status[i][0] != '0':
            res += 1
            # print(cells_status[i][0])
    return res