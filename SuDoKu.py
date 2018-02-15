## This code is for SuDoKu Agent.
import math


def DFS():
    print("Begin")
    pass

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

def DFS(arr):
    # input is a 2d array, 81 * 10
    for i in range(81):
        if arr[i][0] != 0:      # this number is fixed
            continue
        for j in range(1,10,1): # 1 to 9
            if arr[i][j] == 0:  # this number is not in the candidate pool
                pass
            # now j is the candidate value for this i cell, check j

        pass
    return ""

def getIJ(idx):
    # idx: 1 ~ 81
    # return index in the grid (i, j), i is the row, j is the column
    idx -= 1
    return math.floor(idx / 9) + 1, idx % 9 + 1

if __name__ == '__main__':
    # load data
    filePath = 'data/sudoku-problems.txt'
    samples = getData(filePath)
    # for key in samples:
    #     print(key, samples[key])

    print(samples[1][0])
    test = samples[1][0]
    input_a = initialMatrix(test)
