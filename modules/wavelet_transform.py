#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 16:14:13 2021

@author: stanislasbucaille
"""
from modules.utils import reshape_1D
import pandas as pd
import numpy as np
import pywt


def wavelet_decomposition(signal, lookback=100, wavelet="db4"):
    list_wd = []
    
    for i in range(lookback, len(signal)):
        signal_lookback = signal[i-lookback:i]
        coeff = pywt.wavedec(signal_lookback, wavelet, mode="per" )
        list_wd.append(reshape_1D(coeff))
        
    col_names = [f'wd_{i}' for i in range(len(list_wd[0]))]
    df_wd = pd.DataFrame(list_wd, columns=col_names)
    return df_wd


def wavelet_smoothing(signal, lookback=10, lookback_wd=100, wavelet="db4", thresh = 0.05):
    smooth_signal = []
    for i in range(lookback_wd, len(signal)):
        signal_lookback_wd = signal[i-lookback_wd:i]

        # Wavelet decomposition
        coeff = pywt.wavedec(signal_lookback_wd, wavelet, mode="per" )
        # Get smooth signal 
        thresh = thresh*np.nanmax(signal_lookback_wd)
        coeff_thresh = [coeff[0]]+[pywt.threshold(i, value=thresh, mode="soft" ) for i in coeff[1:]]
        signal_recomposed = pywt.waverec(coeff_thresh, wavelet, mode="per" )
        
        smooth_signal.append(signal_recomposed[-lookback:])
    
    col_names = [f'smoooth_lag{i}' for i in range(len(smooth_signal[0]))]
    df_smooth_signal = pd.DataFrame(smooth_signal, columns=col_names)
    return df_smooth_signal