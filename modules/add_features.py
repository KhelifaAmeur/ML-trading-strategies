#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 18:37:38 2021

@author: stanislasbucaille
"""

from ta.momentum import AwesomeOscillatorIndicator, RSIIndicator
from ta.volume import VolumeWeightedAveragePrice
from ta.volatility import BollingerBands
from ta.trend import EMAIndicator, CCIIndicator, MACD as MACDIndicator


def add_return(data):
    data['Return'] = data.close.pct_change().shift(-1)
    return data


def add_signal(data, alpha):
    s_pos = (data.Return > alpha) * (1)
    s_neg = (data.Return < -alpha) * (-1)
    data['Signal'] = s_pos + s_neg
    return data


def add_technical_indicators(data, lookback_period=30):
    AOI = AwesomeOscillatorIndicator(high=data.high, low=data.low,
                                     window1=5, window2=lookback_period)
    VWAP = VolumeWeightedAveragePrice(high=data.high, low=data.low, close=data.Close, volume=data.Volume,
                                      window=lookback_period)
    RSI = RSIIndicator(close=data.close, window=lookback_period)
    BB = BollingerBands(close=data.close, window=lookback_period, window_dev=2)
    EMA = EMAIndicator(close=data.close, window=lookback_period)
    CCI = CCIIndicator(high=data.high, low=data.low, close=data.close, window=lookback_period)
    MACD = MACDIndicator(close=data.close, window_slow=lookback_period, window_fast=7)

    data['MOM'] = AOI.awesome_oscillator()
    # df['MOM_ret'] = df.apply(lambda row: np.log(row.MOM), axis=1)
    data['RSI'] = RSI.rsi()
    data['VWAP'] = VWAP.volume_weighted_average_price()
    data['BB_high'] = BB.bollinger_hband()
    data['BB_low'] = BB.bollinger_lband()
    data['EMA'] = EMA.ema_indicator()
    data['CCI'] = CCI.cci()
    data['MACD'] = MACD.macd()['MOM'] = AOI.awesome_oscillator()

    return data
