#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 18:38:58 2021

@author: stanislasbucaille
"""
import numpy as np

'''
Metrics de performance
    - SharpeRatio: ...
    - MaxDrawback: ...
    - WinLossRatio: ...
    - CumulativeProfit: ...
    - MeanReturn:  ...

Input: (vector of profit)
Output: (float)
'''


def SharpeRatio(profit):
    mean_profit = np.mean(profit)
    var_profit = np.std(profit)
    return mean_profit/var_profit


def MaxDrawback(profit):
    drawback = min(profit)
    return drawback
    
    
def WinLossRatio(profit):
    win = sum(profit>0)
    loss = sum(profit<0)
    return win/loss


def CumulativeProfit(profit):
    cum_profit = sum(profit)
    return cum_profit


def MeanProfit(profit):
    mean_profit = np.mean(profit)
    return mean_profit