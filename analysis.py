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

    t2 = getArray(steps, 0, 0)  # For A* that beam width = inf
    t3 = getArray(steps, 1, 0)  #
    print(t0, t1, t2, t3)

    fig1 = plt.gcf()
    plt.plot(sizeNums, t0, label="A* non-admissible Heuristics")
    plt.plot(sizeNums, t1, label="A* admissible Heuristics")

    plt.plot(sizeNums, t2, label="Bean Search (bw=25) non-admissible Heuristics")
    plt.plot(sizeNums, t3, label="Bean Search (bw=25) admissible Heuristics")

    plt.xlabel("Problem Size")
    plt.ylabel("# of Nodes")
    plt.legend()
    plt.title("Number of nodes searched against the problem size")
    plt.show()
    fig1.savefig("nodesNum_problemSize.png")
    plt.close()

    # plot the CpuTime_problemSize
    t0 = getArray(cpuTimes, 0, beamSize)  # For A* that beam width = inf
    t1 = getArray(cpuTimes, 1, beamSize)  #

    t2 = getArray(cpuTimes, 0, 4)  # For A* that beam width = inf
    t3 = getArray(cpuTimes, 1, 4)  #
    # print(t1)
    print(t0, t1, t2, t3)
    plt.plot(sizeNums, t0, label="A* non-admissible Heuristics")
    plt.plot(sizeNums, t1, label="A* admissible Heuristics")

    plt.plot(sizeNums, t2, label="Bean Search (bw=25) non-admissible Heuristics")
    plt.plot(sizeNums, t3, label="Bean Search (bw=25) admissible Heuristics")

    plt.xlabel("Problem Size")
    plt.ylabel("CPU time")
    plt.legend()
    plt.title("CPU time against the problem size")
    plt.show()
    fig1.savefig("CPUtime_problemSize.png", bbox_inches='tight')
    # plt.close()

    #Table about average solution length
    pass



if __name__ == '__main__':
    # read numpy data
    cpuTimes = np.load('cpuTimes.npy')
    steps = np.load('steps.npy')
    pathes = np.load('pathes.npy')



    plotResult(cpuTimes, steps, pathes)