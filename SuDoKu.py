## This code is for SuDoKu Agent.
import math




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

def initialMatrix(str):
    # return a 81 * 10 array
    # if the cell i has value:
    #       res[i][0] = value, res[i][1:10] = [1] * 9
    # else:
    #       res[i][0] = 0, res[i][1:10] = 0
    res = [[ 0 for x in range(10)] for y in range(81)]
    for i in range(81):
        if str[i] == '0':
            res[i][1:10] = [1] * 9
        else:
            res[i][0] = int(str[i])
    return res

def DFS(arr1):
    # input is a 2d array, 81 * 10
    vistied = [False] * 81
    findResult = False
    arr = initialMatrix(arr1)
    print("Initial SuDoKu")
    cleanPrint81(arr)
    for i in range(81):

        if arr[i][0] != 0:      # this number is fixed
            findResult = True
            continue
        # Then DFS
        if not helper(i, arr):
            findResult = False
            break
        findResult = True
    print("\n\nResult SuDoKu is find == %s"%findResult)
    cleanPrint81(arr)
    return findResult

def helper(i, arr):
    # this is the helper for DFS recursion
    if i > 80:
        return True

    if arr[i][0] != 0:
        return True

    for j in range(1, 10, 1):  # 1 to 9
        if arr[i][j] == 0:  # this number is not in the candidate pool
            pass
        # now j is the candidate value for this i cell, check j
        if matchRules(i, j, arr):  # if i, j match all the rules, then the cell get this j
            oldStatus = update(i, j, arr)       # then update this cell, and check if it match will all others
            idx = 0
            while idx < 81:                     # check all 81 cells, if they all agree or not with this assignment
                if helper(idx, arr):            # if one cell agree, then continue to check next one
                    idx += 1
                    continue
                deUpdate(i, oldStatus, arr)     # otherwise, break this assignment, and retrieve arr
                break
            if idx == 81:                       # all 81 cells agree with this assignment
                return True
    return False


def test(arr):
    arr[0] = 10


def matchRules(i, j, arr):
    # if put j in cell will match with all constraints, then return True, otherwise, return false
    return rule1(i, j, arr) and rule2(i, j, arr) and rule3(i, j, arr) and rule4(i, j, arr)

def rule4(i, j, arr):
    return True

def rule1(i, j, arr):
    # check the same row
    for colIdx in range(9):
        idx = (i//9) * 9 + colIdx
        if idx == i:
            continue
        if j == arr[idx][0]:
            return False
    return True

def rule2(i, j, arr):
    # check the same colum
    for colIdx in range(9):
        jdx = i % 9 + colIdx * 9
        if jdx == i:
            continue
        if j == arr[jdx][0]:
            return False
    return True

def rule3(i, j, arr):
    # check the same cubic 3X3
    # go back to first cell in squire
    domain = getCellSquare(i)
    for idx in domain:
        if idx == i:
            continue
        if j == arr[idx][0]:
            return False
    return True

def getCellSquare(i):
    # square 1
    if i in [i for j in (range(0,3), range(9,12), range(18, 21)) for i in j]:
        return [i for j in (range(0,3), range(9,12), range(18, 21)) for i in j]
    # square 2
    if i in [i for j in (range(3,6), range(12,15), range(21, 24)) for i in j]:
        return [i for j in (range(0,3), range(12,15), range(21, 24)) for i in j]
    # square 3
    if i in [i for j in (range(6,9), range(15,18), range(24, 27)) for i in j]:
        return [i for j in (range(6,9), range(15,18), range(24, 27)) for i in j]

    # square 4
    if i in [i for j in (range(27,30), range(36,39), range(45, 48)) for i in j]:
        return [i for j in (range(27,30), range(36,39), range(45, 48)) for i in j]
    # square 5
    if i in [i for j in (range(30,33), range(39,42), range(48, 51)) for i in j]:
        return [i for j in (range(30,33), range(39,42), range(48, 51)) for i in j]
    # square 6
    if i in [i for j in (range(33,36), range(42,45), range(51, 54)) for i in j]:
        return [i for j in (range(33,36), range(42,45), range(51, 54)) for i in j]

    # square 7
    if i in [i for j in (range(54,57), range(63,66), range(72, 75)) for i in j]:
        return [i for j in (range(54,57), range(63,66), range(72, 75)) for i in j]
    # square 8
    if i in [i for j in (range(57,60), range(66,69), range(75, 78)) for i in j]:
        return [i for j in (range(57,60), range(66,69), range(75, 78)) for i in j]
    # square 9
    if i in [i for j in (range(60,63), range(69,72), range(78, 81)) for i in j]:
        return [i for j in (range(60,63), range(69,72), range(78, 81)) for i in j]
    return []

def update(i, j, arr):
    # update the cell i.
    # return the candidates, for future retrieve
    arr[i][0] = j
    res = arr[i][1:10]
    arr[i][1:10] = [0] * 9
    return res

def deUpdate(i, oldStatus, arr):
    # return to previous status for that cell
    arr[i][0] = 0
    arr[i][1:10] = oldStatus

def getIJ(idx):
    # idx: 0 ~ 80
    # return index in the grid (i, j), i is the row, j is the column
    idx -= 1
    return math.floor(idx / 9), idx % 9

def cleanPrint81(arr):
    res = ""
    for i in range(81):
        if i % 9 == 0:
            res += '\n'
        res += str(arr[i][0])
    print res

if __name__ == '__main__':
    # load data
    filePath = 'data/sudoku-problems.txt'
    samples = getData(filePath)
    # for key in samples:
    #     print(key, samples[key])

    # print(samples[1][0])

    # for i in range(1, 50):
    #     # print(i)
    #     test = samples[i][0]
    #     print(DFS(test))
    test = samples[13][0]
    DFS(test)

