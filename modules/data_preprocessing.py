#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 18:36:52 2021

@author: stanislasbucaille
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def treat_date(date):
    if 'AM' in date or 'PM' in date:
        return date[:-3] + ':00'
    else:
        return date[:-3]


def clean_data(data):
    data['date'] = data['date'].apply(treat_date)
    data = data[::-1].reset_index()
    data = data.drop(['unix', 'symbol', 'index', 'tradecount', 'date', 'Volume BTC'], axis=1)
    return data


def split_data(data, split=0.2):
    n = data.shape[0]
    train_data = data[:-int(split * n)].copy()
    test_data = data[-int(split * n):].copy().reset_index(drop=True)
    return train_data, test_data


def scale_data(train_data, test_data):
    scaler = MinMaxScaler()
    train_data = scaler.fit_transform(train_data)
    test_data = scaler.transform(test_data)
    return train_data, test_data


def prepare_data_for_training(data, lookback_period=10, signal=False):
    # take return and signal
    R = data.loc[lookback_period:, 'Return'].values
    S = None
    if signal:
        S = data.loc[lookback_period:, 'Signal'].values

    # build the dataset for neural networks type models
    if signal:
        df = data.copy().drop(['Return', 'Signal'], axis=1)
    else:
        df = data.copy().drop(['Return'], axis=1)

    X = []
    for i in range(lookback_period, data.shape[0]):
        X.append(df.loc[i - lookback_period:i - 1].values)

    return np.array(X), S, R


def flat(arr):
'''Returns an array with a feature corresponding to each day and each indicator'''
    res = []
    for item in arr:
        features = []
        for day in item:
            features += day.tolist()
        res.append(features)
    return res


def prepare_data_2D_format(data, lookback_period = 10, signal=True):
''' Returns a single dataset ready to be used for logit, CART and Random Forest'''
    # reformatting the data
    X_train, y_train, return_train = prepare_data_for_training(data, lookback_period, signal)
    
    # removing the lookback_period from the beginning
    y_train = y_train[lookback_period:]
    
    ## Remove empty lists in the beginning
    while len(X_train[0]) == 0:
        X_train = X_train[1:]
        y_train = y_train[1:]
    
    X_train = flat(X_train)
    
    ## Some indicators have a larger lookback period than other. 
    ## We remove the beginning of the dataset to make everything homogeneous

    while len(X_train[0]) != lookback_period*len(data.columns):
        X_train = X_train[1:]
        y_train = y_train[1:]

    
    ## Generating a columns name
    features = []
    for k in range(lookback_period):
        features = features + [col+"_day_minus"+str(10-k) for col in data.columns]
        
    train = pd.DataFrame(X_train)
    train.columns = features
    train['Signal'] = pd.Series(y_train)
    
    return train 

def undersampling(data):
'''Returns balanced dataset using undersampling'''
    return