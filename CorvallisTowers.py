## This code is used for CSf531 2018 Winter Coding Assignment #2
## Author: Liqiang He, Eugene Seo
import time
from pathlib import Path
from heapq import heapify, heappop, heappush
import numpy as np
# NMAX = 10

def readData(file):
    res = []
    with open(file, "r") as f:
        lines = f.readlines()
        for line in lines:
            cleanLine = line.strip('\n')
            res.append(cleanLine)
    return res

def finalState(data):
    # return the final state of give state representation
    # 2310 -- > 3210
    goal = ''.join(sorted(data, reverse=True))
    return encodeState(goal, "_", "_")

def find_index_mismatch_peg1(curr, final):
    # print("disks in the peg:", curr)
    # compare from the bottom
    s1 = curr[::-1]
    s2 = final[::-1]
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            return i
    return len(curr)

def compute_gap_between_any_pair_disks(curr):
    # print("disks in the peg:", curr)
    total_gap = 0
    for i in range(len(curr)):
        for j in range(i+1, len(curr)):
            if int(curr[i]) > int(curr[j]):
                total_gap += int(curr[i])-int(curr[j])
    return total_gap

def heuristic_admissiable(curr, final):
    cur1, cur2, cur3 = decodeState(curr)
    cur1 = cur1.replace("_", "")
    cur2 = cur2.replace("_", "")
    cur3 = cur3.replace("_", "")
    final1, final2, final3 = decodeState(final)

    i = find_index_mismatch_peg1(cur1, final1)
    gap1 = (len(cur1) - i) * 2
    # print("gap1:", gap1)

    gap2 = compute_gap_between_any_pair_disks(cur2)
    gap2 += len(cur2)
    # print("gap2:", gap2)

    gap3 = compute_gap_between_any_pair_disks(cur3)
    gap3 += len(cur3)
    # print("gap3:", gap3)

    return gap1 + gap2 + gap3

def heuristic_non_admissiable(curr, final):
    # curr: current state   --> 0+1+2
    # final: final state    --> 210+_+_
    # return 210 - 0 + 1 - 0 + 2 - 0 = 213
    cur1, cur2, cur3 = decodeState(curr)
    final1, final2, final3 = decodeState(final)
    cur1 = 0 if cur1 == "_" else int(cur1)
    cur2 = 0 if cur2 == "_" else int(cur2)
    cur3 = 0 if cur3 == "_" else int(cur3)
    final1 = 0 if final1 == "_" else int(final1)
    final2 = 0 if final2 == "_" else int(final2)
    final3 = 0 if final3 == "_" else int(final3)
    # print (cur1, cur2, cur3 , final1, final2, final3, final1 - final2 - final2 - cur1 + cur2 + cur3 )
    return  final1 - final2 - final3 - cur1 + cur2 + cur3
    # return  final1  - cur1

def encodeState(peg1, peg2, peg3):
    return peg1+","+peg2+","+peg3
    pass

def decodeState(state):
    str = state.split(',')
    peg1 = str[0] if str[0] != '_' else "_"
    peg2 = str[1] if str[1] != '_' else "_"
    peg3 = str[2] if str[2] != '_' else "_"
    return [peg1, peg2, peg3]

def moveOneStep(state, start, end):
    # state: current state: 012+_+
    # start: 0
    # end: 1, or 2
    pegs = decodeState(state)
    if pegs[start] == "_":
        # print("empty peg!")
        return state
    if pegs[end] == '_':
        pegs[end] = pegs[start][0]
    else:
        pegs[end] = pegs[start][0] + pegs[end]
    if len(pegs[start]) == 1:
        pegs[start] = '_'
    else:
        pegs[start] = pegs[start][1:]
    # print(pegs)
    return encodeState(pegs[0], pegs[1],pegs[2])

def findPath(pathes, curState):
    res = list()
    res.append(curState)
    while curState in pathes:
        parentState = pathes[curState]
        res.append(parentState)
        curState = parentState
    return res[::-1]

def solution1(data, funtionID=0, beanWidth=1000):
    # f(n) = g(n) + h(n)
    # h(n) = heuristic1()
    curState = encodeState(data, "_", "_")
    # print("curState: ", curState)
    goalState = finalState(data)
    # print("goalState:", goalState)
    # moveOneStep(initState, 1,2)
    # global NMAX

    NMAX =  100000
    steps = 0
    frontier = []
    heapify(frontier)
    fvalue = 0
    gvalue = 0
    heappush(frontier, (fvalue, gvalue, curState))
    visited = set()
    visited.add(curState)
    pathes = dict() # used to store the path relationship between nodes
    t1 = float(time.clock())
    while curState != goalState and NMAX != 0 and frontier != []:
        NMAX -= 1
        steps += 1
        gvalue += 1
        fvalue, gvalue, curState= heappop(frontier)
        # if curState == goalState:
        #     print("find it!")
        #     break
        # print("state=", curState, "   fvalue=", fvalue, "  num=", NMAX, " goal=", goalState)

        for (i,j) in [(0,1), (0,2), (1,2), (1,0), (2,0), (2,1)]:
            if len(frontier) >= beanWidth:              ### control the beam width
                break
            newState = moveOneStep(curState, i, j)
            if newState in visited:
                continue
            visited.add(newState)
            if funtionID == 1:                          ### control of different heuristic function h
                fvalue = gvalue + heuristic_admissiable(newState, goalState)
            else:
                fvalue = gvalue + heuristic_non_admissiable(newState, goalState)

            heappush(frontier, (fvalue, gvalue, newState))
            pathes[newState] = curState

    t2 = float(time.clock())
    path = []
    if NMAX == 0:
        # print(NMAX == 0)
        # print(" Failed of exhausted all tries for %s, more steps needed.. "%data)
        pass
    elif curState != goalState:
        # print("Failed, cannot reach the goal from %s"%data)
        pass
    else:
        # print("Passed, goal of %s is found "%data)
        # print(curState, goalState)
        path = findPath(pathes, curState)
        # print(" Finished! \n Path length %d with steps = %d: ... "%(len(path), steps))
        # print(path)
        # print("Done")
    print("Finished funtionID = %d and beanWidth = %f for data = %s"%(funtionID, float(beanWidth), data))
    return t2-t1, steps, path
    # print(" CPU time:", t2-t1)

def saveFiles(cpuTimes, steps, pathes):
    np.save("cpuTimes", cpuTimes)
    np.save("steps", steps)
    np.save("pathes", pathes)
    pass

if __name__ == '__main__':
    ## configuration: disk number
    ##
    filePath = "data/4.txt"
    data = readData(filePath)
    print(solution1("012345",0,float("inf")))
    '''
    sizeNums = [4, 5, 6, 7, 8, 9, 10]            # test for different number of disks
    beamSizes = [5, 10, 15, 20, 25, 50, 100, float("inf")]    # test for different beam widths
    functionIDS = [0, 1]                        # test for different function id
    ele0 = [[] for _ in range(20)]
    ele1 = [ele0 for _ in sizeNums]
    ele2 = [ele1 for _ in beamSizes]
    # steps = [ele2 for _ in functionIDS]
    # cupTimes = [ele2 for _ in functionIDS]
    pathes = [ele2 for _ in functionIDS]
    steps = np.ndarray(shape=(len(functionIDS),
                             len(beamSizes),
                             len(sizeNums),
                             20))
    cupTimes = np.ndarray(shape=(len(functionIDS),
                              len(beamSizes),
                              len(sizeNums),
                              20))
    # pathes = np.ndarray(shape=(len(functionIDS),
    #                           len(beamSizes),
    #                           len(sizeNums),
    #                           20))
    for kdx, functionID in enumerate(functionIDS):
        for idx, beamSize in enumerate(beamSizes):
            for jdx, sizeNum in enumerate(sizeNums):
                for p in range(20):
                    filePath = 'data/'+str(sizeNum) +'.txt'
                    if not Path(filePath).exists():
                        continue
                    data = readData(filePath)
                    res = solution1(data[p], funtionID=functionID, beanWidth=beamSize)
                    cupTimes[kdx][idx][jdx][p] = res[0]
                    steps[kdx][idx][jdx][p] = res[1]
                    pathes[kdx][idx][jdx][p] = res[2]

    saveFiles(cupTimes, steps, np.asarray(pathes))

    '''

    pass