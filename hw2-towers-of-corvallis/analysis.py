## This code is used for CSf531 2018 Winter Coding Assignment #2
## Author: Liqiang He, Eugene Seo
## analysis of the result
import numpy as np
import matplotlib.pyplot as plt
cpuTimes = np.load('cpuTimes.npy')
steps = np.load('steps.npy')
pathes = np.load('pathes.npy')

# print(pathes)

def getArray(array, functionID, beamSize):
    temp = array[functionID][beamSize]
    res = []
    for ele in temp:
        # print(ele)
        res.append(np.mean(ele))
    return res
def getArrayPathLength(array, functionID, beamSize):
    temp = array[functionID][beamSize]
    res = []
    ratio = []
    for twenty in temp:
        # print(ele)
        val = 0
        count = 0
        for one in twenty:
            val += one
            if one != 0:
                count += 1
        if count == 0:
            res.append(2000)
        else:
            res.append(val/count)
        ratio.append(count/20)
    return res, ratio

def getBeamWidth(array, functionID, probSize):
    temp = array[functionID]
    res = []
    for oneBeam in temp:
        # print(oneBeam[probSize])
        res.append(np.mean(oneBeam[probSize]))
    return res

def getBeamWidthLen(array, functionID, probSize):
    temp = array[functionID]
    res = []
    ratio = []
    for oneBeam in temp:
        count = 0
        val = 0
        for one in oneBeam[probSize]:
            val += one
            if val != 0:
                count += 1
        if count == 0:
            res.append(2000)
        else:
            res.append(val/count)
        ratio.append(count/20)
    return res, ratio

    pass


def plotResult(cpuTimes, steps, pathes):
    sizeNums = [4, 5, 6, 7, 8, 9, 10]  # test for different number of disks
    beamSizes = [5, 10, 15, 20, 25, 50, 100, float("inf")]  # test for different beam widths
    functionIDS = [0, 1]
    beamSize = 7 # select inf
    # plot the number of nodes (steps)
    # steps = np.ndarray(shape=(len(functionIDS),
    #                           len(beamSizes),
    #                           len(sizeNums),
    #                           20))

    # plot the nodesNum_problemSize
    t0 = getArray(steps, 0, beamSize)       #   For A* that beam width = inf, averaged number
    t1 = getArray(steps, 1, beamSize)       #

    t2 = getArray(steps, 0, 6)  # For A* that beam width = inf
    t3 = getArray(steps, 1, 6)  #
    print(t0, t1, t2, t3)

    fig1 = plt.gcf()
    plt.plot(sizeNums, t0, label="A* non-admissible Heuristics")
    plt.plot(sizeNums, t1, label="A* admissible Heuristics")

    plt.plot(sizeNums, t2, label="Bean Search (bw=100) non-admissible Heuristics")
    plt.plot(sizeNums, t3, label="Bean Search (bw=100) admissible Heuristics")

    plt.xlabel("Problem Size")
    plt.ylabel("# of Nodes")
    plt.legend(loc=2, fontsize=8.5)
    plt.title("Number of nodes searched against the problem size")
    plt.show()
    fig1.savefig("resultPlots/nodesNum_problemSize.png")
    plt.close()

    # plot the CpuTime_problemSize
    t0 = getArray(cpuTimes, 0, beamSize)  # For A* that beam width = inf
    t1 = getArray(cpuTimes, 1, beamSize)  #

    t2 = getArray(cpuTimes, 0, 6)  # For A* that beam width = inf
    t3 = getArray(cpuTimes, 1, 6)  #
    # print(t1)
    print(t0, t1, t2, t3)
    fig1 = plt.gcf()
    plt.plot(sizeNums, t0, label="A* non-admissible Heuristics")
    plt.plot(sizeNums, t1, label="A* admissible Heuristics")

    plt.plot(sizeNums, t2, label="Bean Search (bw=100) non-admissible Heuristics")
    plt.plot(sizeNums, t3, label="Bean Search (bw=100) admissible Heuristics")

    plt.xlabel("Problem Size")
    plt.ylabel("CPU time")
    plt.legend(loc=2, fontsize=8.5)
    plt.title("CPU time against the problem size")
    plt.show()
    fig1.savefig("resultPlots/CPUtime_problemSize.png", bbox_inches='tight')
    # plt.close()

    #Figure about average solution length

    #  Plot the average solution length
    t0, ratio0 = getArrayPathLength(pathes, 0, beamSize)  # For A* that beam width = inf, averaged number
    t1, ratio1 = getArrayPathLength(pathes, 1, beamSize)  #

    t2, ratio2 = getArrayPathLength(pathes, 0, 6)  # For A* that beam width = inf
    t3, ratio3 = getArrayPathLength(pathes, 1, 6)  #
    print(t0, t1, t2, t3)

    print(t0)
    print(t1)
    print(t2)
    print(t3)

    print(ratio0)
    print(ratio1)
    print(ratio2)
    print(ratio3)
    fig1 = plt.gcf()
    plt.plot(sizeNums, t0, label="A* non-admissible Heuristics")
    plt.plot(sizeNums, t1, label="A* admissible Heuristics")

    plt.plot(sizeNums, t2, label="Bean Search (bw=100) non-admissible Heuristics")
    plt.plot(sizeNums, t3, label="Bean Search (bw=100) admissible Heuristics")

    plt.xlabel("Problem Size")
    plt.ylabel("Average Solution Length")
    plt.legend(loc=2, fontsize=8.5)
    plt.title("Average solution length against the problem size")
    plt.show()
    fig1.savefig("resultPlots/aveSoluLen_problemSize.png")
    plt.close()

    ## plot the beam width impact, fix problem size = 7
    ## so function select 1, 2, beam size vary, problem size fixed as 9 == (idx=5)
    # t0 = getBeamWidth(steps, 0, 5)              # function 0, 3 NonAdmissible
    # t1 = getBeamWidth(steps, 1, 5)              # function 1, 3
    #
    # print(t0, t1)
    t0, ratio0 = getBeamWidthLen(pathes, 0, 5)    # function 0, 3 NonAdmissible
    t1, ratio1 = getBeamWidthLen(pathes, 1, 5)    # function 1, 3
    print(t0, t1)
    print(ratio0, ratio1)
    ## beam width vs CPU time
    t0 = getBeamWidth(cpuTimes, 0, 5)
    t1 = getBeamWidth(cpuTimes, 1, 5)
    print(t0, t1)
    pass

# def plotResult1(cpuTimes, steps, pathes):
#     sizeNums = [4, 5, 6, 7, 8, 9, 10]  # test for different number of disks
#     beamSizes = [5, 10, 15, 20, 25, 50, 100, float("inf")]  # test for different beam widths
#     functionIDS = [0, 1]
#     beamSize = 7 # select inf
#     # plot the number of nodes (steps)
#     # steps = np.ndarray(shape=(len(functionIDS),
#     #                           len(beamSizes),
#     #                           len(sizeNums),
#     #                           20))
#
#     # plot the nodesNum_problemSize
#     # t0 = getArrayPathLength(pathes, 0, beamSize)
#     print(pathes[0][7][1][2])
#     pass

if __name__ == '__main__':
    # read numpy data
    cpuTimes = np.load('result/cpuTimes2.npy')
    steps = np.load('result/steps2.npy')
    pathes = np.load('result/pathes2.npy')



    plotResult(cpuTimes, steps, pathes)