#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 18:38:11 2021

@author: stanislasbucaille
"""
import numpy as np
import pandas as pd

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

'''
---------------
Classification
---------------
Metrics de prediction
    - Acc:
    - WAcc:
    - TPR:
    - FPR:
    - F1_score:

Input: (y_true, y_pred, w_true=optional) | vector of {-1, 0, 1}
Output: (float)
'''


def get_confusion_matrix(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    return cm

def get_TPR_FPR(y_true, y_pred):
    TPRs = recall_score(y_true, y_pred, average=None)
    #FPRs = ...
    return TPRs, #FPRs


def get_ACC(y_true, y_pred):
    acc = accuracy_score(y_true, y_pred)
    return acc


def get_F1(y_true, y_pred):
    f1 = f1_score(y_true, y_pred)
    return f1


def get_WACC(y_true, y_pred, w_true):
    weights = abs(w_true).sum()
    wacc = abs(w_true)[y_true == y_pred].sum()
    return wacc/weights


'''
-----------
Regression
-----------
Metrics de prediction
    - MSE:
    - MAE:
    - OSR2:

Input: (y_true, y_pred) | vector of float
Output: (float)
'''


def get_MSE(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    return mse


def get_MAE(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    return mae


def get_OSR2(y_true, y_pred, y_true_train):
    sse = np.sum((y_true - y_pred)**2)
    sst = np.sum((y_true - np.mean(y_true_train))**2)
    osr2 = 1 - sse/sst
    return osr2


