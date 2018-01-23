import matplotlib.pyplot as plt


def plotResult():


    a1, b1 = [0 for _ in range(500)], [0 for _ in range(500)]
    def addTogether(aa1, bb1):
        l1 = len(aa1)
        print("empty!  %d" % l1)
        if l1 == 0:

            pass
        l2 = 500
        for i in range(min(500, l2)):
            if i < l1:
                a1[i] += aa1[i]
                b1[i] += bb1[i]
            else:
                a1[i] += aa1[l1 - 1]
                b1[i] += bb1[l1 - 1]



    for i in range(50):
        if i == 32:
            continue
        fileName = "data/random2_agent%d_%d.txt" % (2, i)
        aa1, bb1 = _readFile(fileName)

        addTogether(aa1, bb1)
    a1 = [i/49 for i in a1]
    b1 = [i/49 for i in b1]
    plt.plot(range(500), a1, label="Env1")
    plt.plot(range(500), b1, label="Env2")
    plt.xlabel("Actions taken")
    plt.ylabel("# of clean cells")
    plt.legend()
    plt.title("Performance for Agent#2 averaged 50 trials")
    plt.show()
    plt.savefig("Agent3_1.png")
    plt.close()

def _readFile(fileName):
    a1 = []
    b1 = []

    with open(fileName, "r") as f:
        lines = f.read().splitlines()
        for line in lines:
            # print(line)
            oneLine = line.split('+')
            # print(len(oneLine))
            if(int(oneLine[0]) == 0):
                print("SEE zero %s"%oneLine)
                continue

            a1.append(int(oneLine[1]))
            b1.append(int(oneLine[4]))
    return a1, b1
    pass

if __name__ == '__main__':
    # MyApp().run()
    plotResult()