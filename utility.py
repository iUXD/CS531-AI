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
            res += str(cells_status[i][0])
        else:
            res += '0'
    print(res)

def goalState(cells_status):
    # check if current cells are in goal state
    for i in range(81):
        if cells_status[i][0] == 0 or len(cells_status[i][1]) == 0:
            return False
    return True