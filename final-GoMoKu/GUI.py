#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter
import math
from collections import deque

import Point
import Record
import time
import MCTS
import numpy as np
from Tkinter import Button, Label
from policy_value_net_pytorch import PolicyValueNet
from mcts_alphaZero import MCTSPlayer
from game import Board as Board2
from game import Game

class Chess_Board_Canvas(Tkinter.Canvas):
    # 棋盤繪製
    def __init__(self, master=None, height=0, width=0):
        Tkinter.Canvas.__init__(self, master, height=height, width=width)
        self.step_record_chess_board = Record.Step_Record_Chess_Board()
        # 初始化記步器
        self.height = 15
        self.width = 15
        self.init_chess_board_points()  # 畫點
        self.init_chess_board_canvas()  # 畫棋盤
        self.board = MCTS.Board()
        self.n_in_row = 5
        self.n_playout = 400  # num of simulations for each move
        self.c_puct = 5


        """
        Important 1: Python is pass by reference
        So the self.board will be modified by other operations
        """
        self.AI = MCTS.MonteCarlo(self.board, 1)
        self.AI_1 = MCTS.MonteCarlo(self.board, 0)
        self.clicked = 1
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
        if (self.clicked == 1):

            for i in range(15):
                for j in range(15):
                    square_distance = math.pow((event.x - self.chess_board_points[i][j].pixel_x), 2) + math.pow(
                        (event.y - self.chess_board_points[i][j].pixel_y), 2)
                    # 計算滑鼠的位置和點的距離
                    # 距離小於14的點

                    if (square_distance <= 200) and (self.step_record_chess_board.checkState(i, j) == None):  # 合法落子位置
                        self.clicked = 0
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
                            self.clicked = 1
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
            if (self.clicked != 1):
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
                self.clicked = 1

    def click2(self):  # click關鍵字重複
        """
        #   Human vs AI
        #   Have to load trained NN
        """
        self.train_or_play = False      # this will lock the "ai vs human" button

        return

    def loadAI(self, init_model):
        """"
        # load AI
        """

        # return
        # self.buffer_size = 10000
        # self.batch_size = 512  # mini-batch size for training
        # self.data_buffer = deque(maxlen=self.buffer_size)
        init_model = "current_policy.model"
        init_model = "best_policy.model"
        init_model = 'best_policy_12000.pt'
        # init_model = 'best_policy200.pt'

        self.result =False

        # self.policy_value_net = PolicyValueNet(self.width,
        #                                        self.height,
        #                                        model_file=False)
        self.policy_value_net = PolicyValueNet(self.width,
                                                   self.height,
                                                   model_file=init_model,
                                               use_gpu=False)

        self.mcts_player = MCTSPlayer(self.policy_value_net.policy_value_fn,
                                      c_puct=self.c_puct,
                                      n_playout=self.n_playout,
                                      is_selfplay=0)
        self.board2 = Board2(width=self.width,
                             height=self.height,
                             n_in_row=self.n_in_row)
        self.board2.init_board(1)
        self.game = Game(self.board2)


    def click3(self):
        """
        ##  Training
        ##  make it self play, AI vs AI, no need to click the mouse, so no need to listen the event
        ##  problem: Let two AIs to play, and learn the NN
        """

        self.train_or_play = True       # this will lock the "ai vs human" button
        self.loadAI(False)
        # self.policy_value_net = PolicyValueNet(self.width,
        #                                        self.height)

        # self.mcts_player = MCTSPlayer(self.policy_value_net.policy_value_fn,
        #                               c_puct=self.c_puct,
        #                               n_playout=self.n_playout,
        #                               is_selfplay=1)
        print(self.width, self.height)

        # self.step += 1
        # # self.train_agents()
        # print("agent1: load")
        self.train_nn_agents()

    def train_nn_agents(self):
        self.step += 1
        print("============agents at steps %d ============"%self.step)
        if (self.clicked == 1):  # Black stone, Gomoku agent, using very good heuristic function
            print("Black begins at step %d, %d>>>>>>>>>>>>>>>>>>>>>" %
                  (self.step, self.step_record_chess_board.who_to_play()))
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
                print("win black in black0!!!!!!!!!!!!!!!!")
                result = 1


            self.board.state = np.copy(self.step_record_chess_board.state)
            self.AI.value = self.step_record_chess_board.value[0]
            self.AI.update(self.board.state)
            # print("temp state, before move", self.AI.value)
            action = self.AI.bestAction()
            x, y = action

            self.create_oval(self.chess_board_points[x][y].pixel_x - 10, self.chess_board_points[x][y].pixel_y - 10,
                             self.chess_board_points[x][y].pixel_x + 10, self.chess_board_points[x][y].pixel_y + 10,
                             fill='black')
            move2 = (self.height - y - 1) * self.width + x

            self.board2.current_player = 1
            self.board2.do_move(move2)
            print("Black, Gomoku takes action: ", move2, x, y, (self.step,self.step_record_chess_board.who_to_play()))
            self.step_record_chess_board.insert_record(x, y)    # this function will switch to another player
            # if (self.step_record_chess_board.value[1][x][y] >= 90000):
            #     print("win white in black")
            #     result = 2
            # if (self.step_record_chess_board.value[2][x][y] >= 90000):
            #     print("win black in black")
            #     result = 1
            m6 = self.board.isWin(self.step_record_chess_board.state, (x, y), 1)
            if result == 1 or m6:
                self.create_text(240, 475, text='the black wins, b11')
                return
            elif result == 2:
                self.create_text(240, 475, text='the white wins, b22')
                return
            self.clicked = 0



        if (self.clicked != 1):                                             # white stone, AlphaZero Angent
            print("White begins at step %d, %d >>>>>>>>>>>>>>>>>>>>>" %
                  (self.step, self.step_record_chess_board.who_to_play()))
            self.clicked = 1
            if self.step_record_chess_board.who_to_play() == 1:
                cur_play = 1
            elif self.step_record_chess_board.who_to_play() == 2:
                cur_play = 2                                                # current is white, 2

            if (self.step_record_chess_board.value[2][x][y] >= 90000):
                print("win white in white!!!!!!!!!!!!!!!!")
                result = 2



            # NN AI do:
            # get board state information
            temp_board = np.copy(self.step_record_chess_board.state)
            self.board2.update_state(temp_board)

            self.board2.current_player = cur_play
            self.mcts_player.reset_player()
            self.mcts_player.set_player_ind(cur_play)
            test_moved = list(set(range(self.width * self.height)) - set(self.board2.availables))
            self.mcts_player.reset_player()
            action = self.mcts_player.get_action(self.board2)
            self.board2.do_move(action)
            x = action % self.width
            y = action // self.height
            y = self.height - y - 1
            # print("after action",self.board2.states, len(self.board2.availables))
            # print("White, NN agent want to place at: ", action, x, y, (self.step,self.step_record_chess_board.who_to_play()))
            # self.board2.do_move(action)
            # insert into the record, for the white player to use
            self.step_record_chess_board.insert_record(x, y)
            # print("----------------------------------------")

            self.create_oval(self.chess_board_points[x][y].pixel_x - 10,
                             self.chess_board_points[x][y].pixel_y - 10,
                             self.chess_board_points[x][y].pixel_x + 10,
                             self.chess_board_points[x][y].pixel_y + 10, fill='white')
            if self.result:
                print("white wins")
                return
            # if (self.step_record_chess_board.value[1][x][y] >= 90000):
            #     print("win white in white")
            #     result = 2
            # if (self.step_record_chess_board.value[2][x][y] >= 90000):
            #     print("win black in white")
            #     result = 1
            m6 = self.board.isWin(self.step_record_chess_board.state, (x, y), 2)
            if result == 1:
                self.create_text(240, 475, text='the black wins, w12')
                return

            elif result == 2 or m6:
                self.create_text(240, 475, text='the white wins, w22')
                return
            self.clicked = 1


        if  self.text_id:
            print(self.text_id)
            self.delete(self.text_id)
        self.text_id = self.create_text(150, 475, text='Step: %d'%self.step)
        self.after(10, self.train_nn_agents)

    def collect_selfplay_data(self, n_games=1):
        """collect self-play data for training"""
        for i in range(n_games):
            winner, play_data = self.game.start_self_play(self.mcts_player,
                                                          temp=1)
            play_data = list(play_data)[:]
            self.episode_len = len(play_data)
            # augment the data
            play_data = self.get_equi_data(play_data)
            self.data_buffer.extend(play_data)

    def get_equi_data(self, play_data):
        """augment the data set by rotation and flipping
                play_data: [(state, mcts_prob, winner_z), ..., ...]
                """
        extend_data = []
        for state, mcts_porb, winner in play_data:
            for i in [1, 2, 3, 4]:
                # rotate counterclockwise
                equi_state = np.array([np.rot90(s, i) for s in state])
                equi_mcts_prob = np.rot90(np.flipud(
                    mcts_porb.reshape(self.height, self.width)), i)
                extend_data.append((equi_state,
                                    np.flipud(equi_mcts_prob).flatten(),
                                    winner))
                # flip horizontally
                equi_state = np.array([np.fliplr(s) for s in equi_state])
                equi_mcts_prob = np.fliplr(equi_mcts_prob)
                extend_data.append((equi_state,
                                    np.flipud(equi_mcts_prob).flatten(),
                                    winner))
        return extend_data



    def train_agents(self):
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
        self.after(10, self.train_agents)


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
        b2 = Button(self, text="AlphaZero vs   AI", command=self.chess_board_canvas.click3)
        b2.pack(side='bottom')
        self.chess_board_label_frame.pack();
        self.chess_board_canvas.pack();
