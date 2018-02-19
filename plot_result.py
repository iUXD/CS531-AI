import matplotlib.pyplot as plt
import numpy as np
def plotResult(file_name):
    idx, fb, mcv, time1, time2 = _readFile(file_name)
    cate = _read_diff()
    # print(idx[0])
    # print(cate)
    #
    cat = []

    for i in range(4):
        tt =  clean_data(cate, fb[i], mcv[i], idx[i])
        cat.append(tt)
        print("====>")
    diffculty = ["Easy", "Medium", "Hard", "Evil"]
    bar_width = 0.3

    #
    # for i in range(4):  # 4 rules
    #     cat_i =cat[i][0]            # easy
    #     fig1 = plt.gcf()
    #
    #
    #     print(cat[i][4], cat[i][4][0], cat[i][4][1])
    #     # print(len(cat_i[:,0]))
    #     plt.bar(range(len(cat_i[:,0])), cat_i[:,0], width = bar_width , color="red", label="FB")
    #     plt.bar(np.array(range(len(cat_i[:, 0]))) - bar_width, cat_i[:, 1], width = bar_width, color="green", label="MCV")
    #     ax = plt.axes()
    #     plt.xticks(range(23), cat_i[:2], color='red')
    #     ax.set_xticklabels(cat_i[:,2])
    #     plt.xlim(0,23)
    #     plt.xlabel("Problems ID")
    #     plt.ylabel("# of backtracks")
    #     plt.legend(loc=2, fontsize=8.5)
    #     plt.title("Number of Backtracks with RuleSet #"+ str(i) +" of " + diffculty[0] +" Problems")
    #     plt.show()
    #     plot_file = "plots/rule_set_"+str(i) + "_" + diffculty[0] + ".png"
    #     fig1.savefig(plot_file)
    #     plt.close()
    #
    #     cat_i = cat[i][1]  # easy
    #     fig1 = plt.gcf()
    #     # print(cat_i)
    #     # print(len(cat_i[:, 0]))
    #     plt.bar(range(len(cat_i[:, 0])), cat_i[:, 0], width=bar_width, color="red", label="FB")
    #     plt.bar(np.array(range(len(cat_i[:, 0]))) - bar_width, cat_i[:, 1], width=bar_width, color="green", label="MCV")
    #     ax = plt.axes()
    #     plt.xticks(range(21), cat_i[:2], color='red')
    #     ax.set_xticklabels(cat_i[:, 2])
    #     plt.xlim(0,21)
    #     plt.xlabel("Problems ID")
    #     plt.ylabel("# of backtracks")
    #     plt.legend(loc=2, fontsize=8.5)
    #     plt.title("Number of Backtracks with RuleSet #" + str(i) + " of " + diffculty[1] + " Problems")
    #     plt.show()
    #     plot_file = "plots/rule_set_" + str(i) + "_" + diffculty[1] + ".png"
    #     fig1.savefig(plot_file)
    #     plt.close()
    #
    #     cat_i = cat[i][2]  # easy
    #     fig1 = plt.gcf()
    #     # print(cat_i)
    #     # print(len(cat_i[:, 0]))
    #     plt.bar(range(len(cat_i[:, 0])), cat_i[:, 0], width=bar_width, color="red", label="FB")
    #     plt.bar(np.array(range(len(cat_i[:, 0]))) - bar_width, cat_i[:, 1], width=bar_width, color="green", label="MCV")
    #     ax = plt.axes()
    #     plt.xticks(range(18), cat_i[:2], color='red')
    #     ax.set_xticklabels(cat_i[:, 2])
    #     plt.xlim(0,18)
    #     plt.xlabel("Problems ID")
    #     plt.ylabel("# of backtracks")
    #     plt.legend(loc=2, fontsize=8.5)
    #     plt.title("Number of Backtracks with RuleSet #" + str(i) + " of " + diffculty[2] + " Problems")
    #     plt.show()
    #     plot_file = "plots/rule_set_" + str(i) + "_" + diffculty[2] + ".png"
    #     fig1.savefig(plot_file)
    #     plt.close()
    #
    #     cat_i = cat[i][3]  # easy
    #     fig1 = plt.gcf()
    #     # print(cat_i)
    #     # print(len(cat_i[:, 0]))
    #     plt.bar(range(len(cat_i[:, 0])), cat_i[:, 0], width=bar_width, color="red", label="FB")
    #     plt.bar(np.array(range(len(cat_i[:, 0]))) - bar_width, cat_i[:, 1], width=bar_width, color="green", label="MCV")
    #     ax = plt.axes()
    #     plt.xticks(range(15), cat_i[:2], color='red')
    #     ax.set_xticklabels(cat_i[:, 2])
    #     plt.xlim(0,15)
    #     plt.xlabel("Problems ID")
    #     plt.ylabel("# of backtracks")
    #     plt.legend(loc=2, fontsize=8.5)
    #     plt.title("Number of Backtracks with RuleSet #" + str(i) + " of " + diffculty[3] + " Problems")
    #     plt.show()
    #     plot_file = "plots/rule_set_" + str(i) + "_" + diffculty[3] + ".png"
    #     fig1.savefig(plot_file)
    #     plt.close()

    # plot
    # # print("===")
    # # print(fb)
    # # print("===")
    # # print(mcv)
    # # print("===")
    # # print(time1)
    # # print("===")
    # # print(time2)
    # res_rule1 = np.array(list(zip(fb[0], mcv[0])))
    # print(res_rule1)
    # fig1 = plt.gcf()
    # bar_width = 0.3
    # colors = ["red", "green"]
    # lb = ["FB", "MCV"]
    # plt.bar(idx[0][1:20],fb[1][1:20], width=bar_width, color="red", label="FB")
    # plt.bar(np.array(idx[0][1:20]) - -bar_width, np.array(mcv[1][1:20]), width=bar_width, color='green', label="MCV")
    # # plt.axis([0, 77, 0, 600])
    #
    # plt.xlabel("Problems ID")
    # plt.ylabel("# of backtracks")
    # plt.legend(loc=2, fontsize=8.5)
    # plt.title("Number of backtracks for each problem with rules set 1(no inference)")
    # plt.show()
    # fig1.savefig("plots/rule_set_1.png")
    # plt.close()
    # plt.bar(range(22), np.random.randn(22,1))
    # plt.show()
    # plt.hist(np.random.randn(10, 2), [0,1,2,3,4,5,6,7,8,9],histtype='bar', color=colors, label=lb)
    # plt.show()
    # print(np.random.randn(10, 2))
    # print(res_rule1[1:10])

    fb_easy = []
    fb_med =[]
    fb_hard = []
    fb_evil = []
    fb_r1 = []
    fb_r2 = []
    fb_r3 = []
    fb_r4 = []
    mcv_r1 = []
    mcv_r2 = []
    mcv_r3 = []
    mcv_r4 = []
    for i in range(4):
        fb_r1.append(cat[0][4 + i][0])
        fb_r2.append(cat[1][4 + i][0])
        fb_r3.append(cat[2][4 + i][0])
        fb_r4.append(cat[3][4 + i][0])
        mcv_r1.append(cat[0][4 + i][1])
        mcv_r2.append(cat[1][4 + i][1])
        mcv_r3.append(cat[2][4 + i][1])
        mcv_r4.append(cat[3][4 + i][1])
    print(fb_r1, fb_r2, fb_r3, fb_r4, mcv_r1, mcv_r2, mcv_r3, mcv_r4)


        # print(cat_i)
        # print(len(cat_i[:, 0]))
    bar_width = 0.2



    fig1 = plt.gcf()
    plt.bar(np.array([1, 2, 3, 4]), fb_r1, width=bar_width, color="red", label="Rule Set 1")
    plt.bar(np.array([1, 2, 3, 4]) + 1 * bar_width, fb_r2, width=bar_width, color="green", label="Rule Set 2")
    plt.bar(np.array([1, 2, 3, 4]) + 2 * bar_width, fb_r3, width=bar_width, color="blue", label="Rule Set 3")
    plt.bar(np.array([1, 2, 3, 4]) + 3 * bar_width, fb_r4, width=bar_width, color="gray", label="Rule Set 4")
    ax = plt.axes()
    plt.xticks([1.35, 2.35, 3.35, 4.35], diffculty)
    ax.set_xticklabels(diffculty)
    plt.xlim(1,5)
    plt.xlabel("Difficulty Levels")
    plt.ylabel("Averaged Number of backtracks")
    plt.yscale('symlog')
    plt.legend(loc=1, fontsize=8.5)
    plt.title("Averaged Number of Backtracks For Fixed Baseline Heuristic")
    plt.show()
    plot_file = "plots/ave_fb.png"
    fig1.savefig(plot_file)
    plt.close()



    fig1 = plt.gcf()
    plt.bar(np.array([1, 2, 3, 4]), mcv_r1, width=bar_width, color="red", label="Rule Set 1")
    plt.bar(np.array([1, 2, 3, 4]) + 1 * bar_width, mcv_r2, width=bar_width, color="green", label="Rule Set 2")
    plt.bar(np.array([1, 2, 3, 4]) + 2 * bar_width, mcv_r3, width=bar_width, color="blue", label="Rule Set 3")
    plt.bar(np.array([1, 2, 3, 4]) + 3 * bar_width, mcv_r4, width=bar_width, color="gray", label="Rule Set 4")
    ax = plt.axes()
    plt.xticks([1.35, 2.35, 3.35, 4.35], diffculty)
    ax.set_xticklabels(diffculty)
    plt.xlim(1,5)
    plt.xlabel("Difficulty Levels")
    plt.ylabel("Averaged Number of backtracks")
    plt.yscale('symlog')
    plt.legend(loc=1, fontsize=8.5)
    plt.title("Averaged Number of Backtracks For MCV Heuristic")
    plt.show()
    plot_file = "plots/ave_mvc.png"
    fig1.savefig(plot_file)
    plt.close()
    #

    # plot time
    # bar_width = 0.2
    # cat2 = []
    # for i in range(4):
    #     tt = clean_data(cate, time1[i], time2[i], idx[i])
    #     cat2.append(tt)
    #
    # for i in range(4):
    #     fb_r1.append(cat2[0][4 + i][0])
    #     fb_r2.append(cat2[1][4 + i][0])
    #     fb_r3.append(cat2[2][4 + i][0])
    #     fb_r4.append(cat2[3][4 + i][0])
    #     mcv_r1.append(cat2[0][4 + i][1])
    #     mcv_r2.append(cat2[1][4 + i][1])
    #     mcv_r3.append(cat2[2][4 + i][1])
    #     mcv_r4.append(cat2[3][4 + i][1])
    #
    # fig1 = plt.gcf()
    # plt.bar(np.array([1, 2, 3, 4]), fb_r1, width=bar_width, color="red", label="Rule Set 1")
    # plt.bar(np.array([1, 2, 3, 4]) + 1 * bar_width, fb_r2, width=bar_width, color="green", label="Rule Set 2")
    # plt.bar(np.array([1, 2, 3, 4]) + 2 * bar_width, fb_r3, width=bar_width, color="blue", label="Rule Set 3")
    # plt.bar(np.array([1, 2, 3, 4]) + 3 * bar_width, fb_r4, width=bar_width, color="gray", label="Rule Set 4")
    # ax = plt.axes()
    # plt.xticks([1.35, 2.35, 3.35, 4.35], diffculty)
    # ax.set_xticklabels(diffculty)
    # plt.xlim(1, 5)
    # plt.xlabel("Difficulty Levels")
    # plt.ylabel("Averaged Time")
    # plt.yscale('symlog')
    # plt.legend(loc=2, fontsize=8.5)
    # plt.title("Averaged Time For Fixed Baseline Heuristic")
    # plt.show()
    # plot_file = "plots/ave_fb_time.png"
    # fig1.savefig(plot_file)
    # plt.close()
    #
    # fig1 = plt.gcf()
    # plt.bar(np.array([1, 2, 3, 4]), mcv_r1, width=bar_width, color="red", label="Rule Set 1")
    # plt.bar(np.array([1, 2, 3, 4]) + 1 * bar_width, mcv_r2, width=bar_width, color="green", label="Rule Set 2")
    # plt.bar(np.array([1, 2, 3, 4]) + 2 * bar_width, mcv_r3, width=bar_width, color="blue", label="Rule Set 3")
    # plt.bar(np.array([1, 2, 3, 4]) + 3 * bar_width, mcv_r4, width=bar_width, color="gray", label="Rule Set 4")
    # ax = plt.axes()
    # plt.xticks([1.35, 2.35, 3.35, 4.35], diffculty)
    # ax.set_xticklabels(diffculty)
    # plt.xlim(1, 5)
    # plt.xlabel("Difficulty Levels")
    # plt.ylabel("Averaged Time")
    # plt.yscale('symlog')
    # plt.legend(loc=2, fontsize=8.5)
    # plt.title("Averaged Time For MCV Heuristic")
    # plt.show()
    # plot_file = "plots/ave_mvc_time.png"
    # fig1.savefig(plot_file)
    # plt.close()
    pass


def _readFile(fileName):

    m, n = 4, 77
    idx = [[0 for x in range(n)] for y in range(m)]
    fb = [[0 for x in range(n)] for y in range(m)]
    mcv = [[0 for x in range(n)] for y in range(m)]
    time1 = [[0 for x in range(n)] for y in range(m)]
    time2 = [[0 for x in range(n)] for y in range(m)]
    rule_num = 0
    with open(fileName, "r") as f:
        lines = f.read().splitlines()
        for one_line in lines:
            if one_line == "********":
                rule_num += 1
                continue
            one_line = one_line.split(" ")
            i = int(one_line[0])
            idx[rule_num][i] = i
            fb[rule_num][i] = int(one_line[1])
            mcv[rule_num][i] = int(one_line[2])
            time1[rule_num][i] = float(one_line[3])
            time2[rule_num][i] = float(one_line[4])
    return idx, fb, mcv, time1, time2

    #         # print(line)
    #         if
    #         oneLine = line.split('+')
    #         # print(len(oneLine))
    #
    #
    #         a1.append(int(oneLine[1]))
    #         b1.append(int(oneLine[4]))
    # return a1, b1
    pass

def _read_diff():
    file_name = "data/result_diff.txt"
    res = []
    with open(file_name, "r") as f:
        lines = f.read().splitlines()
        for line in lines:
            res.append(line)
    return res

def clean_data(cate, fb, mcv, idx):
    cat1 = []
    cat2 = []
    cat3 = []
    cat4 = []
    for i in range(77):
        if cate[i] == "Easy":
            cat1.append([fb[i], mcv[i], idx[i]])
        if cate[i] == "Medium":
            cat2.append([fb[i], mcv[i], idx[i]])
        if cate[i] == "Hard":
            cat3.append([fb[i], mcv[i], idx[i]])
        if cate[i] == "Evil":
            cat4.append([fb[i], mcv[i], idx[i]])

    cat1 = np.array(cat1)
    cat2 = np.array(cat2)
    cat3 = np.array(cat3)
    cat4 = np.array(cat4)


    cat11 = np.mean(cat1, axis=0)
    cat22 = np.mean(cat2, axis=0)
    cat33 = np.mean(cat3, axis=0)
    cat44 = np.mean(cat4, axis=0)
    # print(cat1)
    # print(cat2)
    # print(cat3)
    # print(cat4)
    return cat1, cat2, cat3, cat4, cat11, cat22, cat33, cat44

if __name__ == '__main__':
    # MyApp().run()
    file_name = "data/result.txt"
    plotResult(file_name)