## This code is used for CSf531 2018 Winter Coding Assignment #2
## Author: Liqiang He, Eugene Seo

from heapq import heapify, heappop, heappush
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
    #return "3210,_,_"
    return encodeState(data[::-1], "_", "_")
    pass

def heuristic_admissiable(curr, final):
    # curr: current state   --> 0+1+2
    # final: final state    --> 210+_+_
    # return 210 - 0 + 1 - 0 + 2 - 0 = 213
    return 0
    pass

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
    return  final1 - final2 - final2 - cur1 + cur2 + cur3
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

def solution1(data):
    # f(n) = g(n) + h(n)
    # h(n) = heuristic1()
    curState = encodeState(data, "_", "_")
    print("curState: ", curState)
    goalState = finalState(data)
    print("goalState:", goalState)
    # moveOneStep(initState, 1,2)
    # global NMAX
    NMAX =  100
    frontier = []
    heapify(frontier)
    fvalue = 0
    gvalue = 0
    heappush(frontier, (fvalue, gvalue, curState))
    visited = set()
    visited.add(curState)
    while curState != goalState and NMAX != 0 and frontier != []:
        NMAX -= 1
        fvalue, gvalue, curState= heappop(frontier)
        # if curState == goalState:
        #     print("find it!")
        #     break
        print("state==", curState, "   fvalue=", fvalue, "  num=", NMAX, " goal =", goalState)
        for (i,j) in [(0,1), (0,2), (1,2), (1,0), (2,0), (2,1)]:
            newState = moveOneStep(curState, i, j)
            if newState in visited:
                continue
            visited.add(newState)
            gvalue += 1
            fvalue = gvalue + heuristic_non_admissiable(newState, goalState)
            heappush(frontier, (fvalue, gvalue, newState))
            # print("state==", curState,";newState = ",newState, "   fvalue=", fvalue, "  num=", NMAX, "i = ", i, " j=",j)

    if NMAX == 0:
        print(" Failed.. ")
    else:
        print(" Finished! \n Path: ... ")

if __name__ == '__main__':
    ## configuration: disk number
    ##
    filePath = "data/4.txt"
    data = readData(filePath)
    solution1("012")
    #solution1(data[0])
    pass