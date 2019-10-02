#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2018/11/8 17:12
# @Author: mild
# @File  : test.py
from turtle import *
ang = 360 / 12
len = 120
for x in range(12):
    if x % 2 == 0:
        color("red")
    else:
        color("black")
    begin_fill()
    forward(len)
    left(ang)
    forward(len)
    left(180 - ang)
    forward(len)
    left(ang)
    forward(len)
    left(180 - ang)
    end_fill()
    left(ang)









































