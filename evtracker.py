#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 20:42:30 2018

@author: ant
"""

import eval7
import pprint

hand = map(eval7.Card, ("As", "Kd"))
villain = eval7.HandRange("2c2s")
board = []
equity_monte = eval7.py_hand_vs_range_monte_carlo(
    hand, villain, board, 1000000
)

equity_exact = eval7.py_hand_vs_range_exact(hand, villain, board)
print(equity_monte)
print(equity_exact)