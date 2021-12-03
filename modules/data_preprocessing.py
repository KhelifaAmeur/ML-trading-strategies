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


def prepare_data_for_training(data, lookback_period=10):
    # take return and signal
    R = data.loc[lookback_period:, 'Return'].values
    S = data.loc[lookback_period:, 'Signal'].values

    # build the dataset for neural networks type models
    df = data.copy().drop(['Return', 'Signal'], axis=1)
    X = []
    for i in range(lookback_period, data.shape[0]):
        X.append(df.loc[i - lookback_period:i - 1].values)

    return np.array(X), S, R
