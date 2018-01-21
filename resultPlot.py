import matplotlib.pyplot as plt


def plotResult():
    fileName1 = "agent1.txt"
    fileName2 = "agent2_used3.txt"
    fileName3 = "agent3.txt"

    a1, a2, a3, b1, b2, b3 =_readFile(fileName3)
    plt.plot(a1, a2, label="Env1")
    plt.plot(b1, b2, label="Env2")
    plt.xlabel("Actions taken")
    plt.ylabel("# of clean cells")
    plt.legend()
    plt.title("Performance for Agent#1")
    plt.show()
    plt.savefig("Agent3_1.png")
    plt.close()
def _readFile(fileName):
    a1 = []
    a2 = []
    a3 = []
    b1 = []
    b2 = []
    b3 = []

    with open(fileName, "r") as f:
        lines = f.read().splitlines()
        for line in lines:
            # print(line)
            oneLine = line.split('+')
            # print(len(oneLine))

            a1.append(int(oneLine[0]))
            a2.append(int(oneLine[1]))
            a3.append(float(oneLine[2]))
            b1.append(int(oneLine[3]))
            b2.append(int(oneLine[4]))
            b3.append(float(oneLine[5]))
    return a1, a2, a3, b1, b2, b3
    pass

if __name__ == '__main__':
    # MyApp().run()
    plotResult()