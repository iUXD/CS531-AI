#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter
import math
import Point
import Record
import time
import MCTS
import numpy as np
from Tkinter import Button, Label


class Chess_Board_Canvas(Tkinter.Canvas):
    # 棋盤繪製
    def __init__(self, master=None, height=0, width=0):
        Tkinter.Canvas.__init__(self, master, height=height, width=width)
        self.step_record_chess_board = Record.Step_Record_Chess_Board()
        # 初始化記步器
        self.init_chess_board_points()  # 畫點
        self.init_chess_board_canvas()  # 畫棋盤
        self.board = MCTS.Board()
        """
        Important 1: Python is pass by reference
        So the self.board will be modified by other operations
        """
        self.AI = MCTS.MonteCarlo(self.board, 2)
        self.AI_1 = MCTS.MonteCarlo(self.board, 1)
        self.clicked = 0
        self.init = True  # first place is given by user (later need to be replaced as a random selection)
        self.train_or_play = True  # True - train, False - play
        self.step = 0
        self.text_id = None

    def init_chess_board_points(self):
        '''
        生成棋盤點,並且對應到像素座標
        保存到 chess_board_points 屬性
        '''
        self.chess_board_points = [[None for i in range(15)] for j in range(15)]

        for i in range(15):
            for j in range(15):
                self.chess_board_points[i][j] = Point.Point(i, j);  # 轉換棋盤座標像素座標
        # self.label_step = Label(self, text="Step")

    def init_chess_board_canvas(self):
        '''
        初始化棋盤
        '''

        for i in range(15):  # 直線
            self.create_line(self.chess_board_points[i][0].pixel_x, self.chess_board_points[i][0].pixel_y,
                             self.chess_board_points[i][14].pixel_x, self.chess_board_points[i][14].pixel_y)

        for j in range(15):  # 橫線
            self.create_line(self.chess_board_points[0][j].pixel_x, self.chess_board_points[0][j].pixel_y,
                             self.chess_board_points[14][j].pixel_x, self.chess_board_points[14][j].pixel_y)
        # 邊界
        self.create_line(self.chess_board_points[2][2].pixel_x, self.chess_board_points[2][2].pixel_y,
                         self.chess_board_points[2][12].pixel_x, self.chess_board_points[2][12].pixel_y, fill="red")
        self.create_line(self.chess_board_points[12][2].pixel_x, self.chess_board_points[12][2].pixel_y,
                         self.chess_board_points[12][12].pixel_x, self.chess_board_points[12][12].pixel_y, fill="red")
        self.create_line(self.chess_board_points[2][12].pixel_x, self.chess_board_points[2][12].pixel_y,
                         self.chess_board_points[12][12].pixel_x, self.chess_board_points[12][12].pixel_y, fill="red")
        self.create_line(self.chess_board_points[2][2].pixel_x, self.chess_board_points[2][2].pixel_y,
                         self.chess_board_points[12][2].pixel_x, self.chess_board_points[12][2].pixel_y, fill="red")

        for i in range(15):  # 交點橢圓
            for j in range(15):
                r = 1
                self.create_oval(self.chess_board_points[i][j].pixel_x - r, self.chess_board_points[i][j].pixel_y - r,
                                 self.chess_board_points[i][j].pixel_x + r, self.chess_board_points[i][j].pixel_y + r);

    def click1(self, event):  # click關鍵字重複
        if self.train_or_play:
            print("In self training, mouse event is not available")
            return
        '''
        Mouse listener function, for the game played between human and AI
        '''
        if (self.clicked != 1):

            for i in range(15):
                for j in range(15):
                    square_distance = math.pow((event.x - self.chess_board_points[i][j].pixel_x), 2) + math.pow(
                        (event.y - self.chess_board_points[i][j].pixel_y), 2)
                    # 計算滑鼠的位置和點的距離
                    # 距離小於14的點

                    if (square_distance <= 200) and (self.step_record_chess_board.checkState(i, j) == None):  # 合法落子位置
                        self.clicked = 1
                        if self.step_record_chess_board.who_to_play() == 1:
                            # 奇數次，黑落子
                            self.create_oval(self.chess_board_points[i][j].pixel_x - 10,
                                             self.chess_board_points[i][j].pixel_y - 10,
                                             self.chess_board_points[i][j].pixel_x + 10,
                                             self.chess_board_points[i][j].pixel_y + 10, fill='black')
                            Tkinter.Canvas.update(self)
                        # 偶數次，白落子
                        elif self.step_record_chess_board.who_to_play() == 2:
                            self.create_oval(self.chess_board_points[i][j].pixel_x - 10,
                                             self.chess_board_points[i][j].pixel_y - 10,
                                             self.chess_board_points[i][j].pixel_x + 10,
                                             self.chess_board_points[i][j].pixel_y + 10, fill='white')

                        result = 0
                        if (self.step_record_chess_board.value[1][i][j] >= 90000):
                            result = 1
                            self.clicked = 0
                        self.step_record_chess_board.insert_record(i, j)
                        # 落子，最多225

                        #######result = self.step_record_chess_board.check()
                        # 判斷是否有五子連珠

                        if result == 1:
                            self.create_text(240, 475, text='the black wins')
                            # 解除左键绑定
                            self.unbind('<Button-1>')
                            # """Unbind for this widget for event SEQUENCE  the
                            #     function identified with FUNCID."""

                        elif result == 2:
                            self.create_text(240, 475, text='the white wins')
                            # 解除左键绑定
                            self.unbind('<Button-1>')
            # 根據價值網路落子
            if (self.clicked == 1):
                x = 0
                y = 0
                max_value = 0
                for i in range(0, 15):
                    for j in range(0, 15):
                        if (self.step_record_chess_board.value[2][i][j] >= 90000):
                            x = i
                            y = j
                            max_value = 99999
                            break;
                        elif (self.step_record_chess_board.value[0][i][j] >= max_value):
                            x = i
                            y = j
                            max_value = self.step_record_chess_board.value[0][i][j]
                if (self.step_record_chess_board.value[2][x][y] >= 90000):
                    result = 2

                self.board.state = np.copy(self.step_record_chess_board.state)
                self.AI.value = self.step_record_chess_board.value[0]
                self.AI.update(self.board.state)
                action = self.AI.bestAction()
                x, y = action

                self.step_record_chess_board.insert_record(x, y)
                self.create_oval(self.chess_board_points[x][y].pixel_x - 10, self.chess_board_points[x][y].pixel_y - 10,
                                 self.chess_board_points[x][y].pixel_x + 10, self.chess_board_points[x][y].pixel_y + 10,
                                 fill='white')
                #######result = self.step_record_chess_board.check()
                # 判斷是否有五子連珠

                if result == 1:
                    self.create_text(240, 475, text='the black wins')
                    # 解除左键绑定
                    self.unbind('<Button-1>')
                # """Unbind for this widget for event SEQUENCE  the
                #     function identified with FUNCID."""

                elif result == 2:
                    self.create_text(240, 475, text='the white wins')
                    # 解除左键绑定
                    self.unbind('<Button-1>')
                self.clicked = 0

    def click2(self):  # click關鍵字重複
        """
        #   Human vs AI
        #   Have to load trained NN
        """
        self.train_or_play = False

        return

    def click3(self):
        """
        ##  Training
        ##  make it self play, AI vs AI, no need to click the mouse, so no need to listen the event
        ##  problem: Let two AIs to play, and learn the NN
        """
        self.train_or_play = True
        self.step += 1
        if (self.clicked != 1):
            x = 0
            y = 0
            max_value = 0
            result = 0
            for i in range(0, 15):
                for j in range(0, 15):
                    if (self.step_record_chess_board.value[1][i][j] >= 90000):
                        x = i
                        y = j
                        max_value = 99999
                        break
                    elif (self.step_record_chess_board.value[0][i][j] >= max_value):
                        x = i
                        y = j
                        max_value = self.step_record_chess_board.value[0][i][j]
            if (self.step_record_chess_board.value[1][x][y] >= 90000):
                result = 2


            """
            Important 2:
            Only below 4 line are interact between the AI agent and the board
            self.board.state = np.copy(self.step_record_chess_board.state)  # make a deep copy of state
            self.AI_1.value = self.step_record_chess_board.value[1]         # assign board information, a 15*15 array
            self.AI_1.update(self.board.state)                              # AI function, do some calculations
            action = self.AI_1.bestAction()                                 # Best actions the AI will make
            """
            self.board.state = np.copy(self.step_record_chess_board.state)
            self.AI_1.value = self.step_record_chess_board.value[1]
            self.AI_1.update(self.board.state)
            action = self.AI_1.bestAction()

            x, y = action

            self.step_record_chess_board.insert_record(x, y)

            self.create_oval(self.chess_board_points[x][y].pixel_x - 10,
                             self.chess_board_points[x][y].pixel_y - 10,
                             self.chess_board_points[x][y].pixel_x + 10,
                             self.chess_board_points[x][y].pixel_y + 10, fill='black')
            if result == 1:
                self.create_text(240, 475, text='the black wins')
                return

            elif result == 2:
                self.create_text(240, 475, text='the white wins')
                return
            self.clicked = 1

            # 根據價值網路落子
        if (self.clicked == 1):  # White stone
            x = 0
            y = 0
            max_value = 0
            for i in range(0, 15):
                for j in range(0, 15):
                    if (self.step_record_chess_board.value[2][i][j] >= 90000):
                        x = i
                        y = j
                        max_value = 99999
                        break
                    elif (self.step_record_chess_board.value[0][i][j] >= max_value):
                        x = i
                        y = j
                        max_value = self.step_record_chess_board.value[0][i][j]

            if (self.step_record_chess_board.value[2][x][y] >= 90000):
                result = 2

            self.board.state = np.copy(self.step_record_chess_board.state)
            self.AI.value = self.step_record_chess_board.value[0]
            self.AI.update(self.board.state)
            action = self.AI.bestAction()
            x, y = action

            self.step_record_chess_board.insert_record(x, y)
            self.create_oval(self.chess_board_points[x][y].pixel_x - 10, self.chess_board_points[x][y].pixel_y - 10,
                             self.chess_board_points[x][y].pixel_x + 10, self.chess_board_points[x][y].pixel_y + 10,
                             fill='white')

            if result == 1:
                self.create_text(240, 475, text='the black wins')

                return
            elif result == 2:
                self.create_text(240, 475, text='the white wins')
                return
            self.clicked = 0

        if  self.text_id:
            print(self.text_id)
            self.delete(self.text_id)
        self.text_id = self.create_text(150, 475, text='Step: %d'%self.step)
        self.after(10, self.click3)


class Chess_Board_Frame(Tkinter.Frame):
    def __init__(self, master=None):
        Tkinter.Frame.__init__(self, master)
        self.create_widgets()

    def create_widgets(self):
        print("create widgets")
        self.chess_board_label_frame = Tkinter.LabelFrame(self, text="Chess Board", padx=5, pady=5)
        self.chess_board_canvas = Chess_Board_Canvas(self.chess_board_label_frame, height=500, width=480)

        self.chess_board_canvas.bind('<Button-1>', self.chess_board_canvas.click1)
        b1 = Button(self, text="Playing  - AI vs Human", command=self.chess_board_canvas.click2)
        b1.pack(side='bottom')
        b2 = Button(self, text="Training     -    AI vs AI", command=self.chess_board_canvas.click3)
        b2.pack(side='bottom')
        self.chess_board_label_frame.pack();
        self.chess_board_canvas.pack();
