#!/usr/bin/env python
#-*- coding: utf-8 -*-

import GUI
import Tkinter
import os
from Tkinter import Button
from policy_value_net_pytorch import PolicyValueNet
def callback():
    cmd = 'python main.py'
    os.system(cmd)
    exit(0)

if __name__ == '__main__':
    print("running frame")
    window = Tkinter.Tk()
    gui_chess_board = GUI.Chess_Board_Frame(window)

    b = Button(window, text="Restart", command=callback)
    # b2 = Button(window, text="Train", command=callback)
    gui_chess_board.pack()
    b.pack()
    # b2.pack()
    window.mainloop()


    # print("done")