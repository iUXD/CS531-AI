#!/usr/bin/env python
#-*- coding: utf-8 -*-

class Point:

    def __init__(self, x, y):
        '''
        棋盤座標和像素座標轉換
        '''
        self.x = x;
        self.y = y;
        self.pixel_x = 30 + 30 * self.x
        self.pixel_y = 30 + 30 * self.y
