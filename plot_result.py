import matplotlib.pyplot as plt

def plotResult():


    pass


def _readFile(fileName):
    idx = []
    fb = []
    mcv = []
    time1 = []
    time2 = []
    rule_num = 4
    with open(fileName, "r") as f:
        lines = f.read().splitlines()
        for line in lines:
            # print(line)
            oneLine = line.split('+')
            # print(len(oneLine))
            if (int(oneLine[0]) == 0):
                print("SEE zero %s" % oneLine)
                continue

            a1.append(int(oneLine[1]))
            b1.append(int(oneLine[4]))
    return a1, b1



if __name__ == '__main__':
    # MyApp().run()
    plotResult()