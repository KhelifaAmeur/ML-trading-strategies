#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 20:15:33 2021

@author: stanislasbucaille
"""
import numpy as np
import random as rd
import pandas as pd


def baseline(data):
    n = data.shape[0]
    s_baseline = np.array([int(rd.random()*3)-1 for i in range(n)])
    s_baseline = pd.Series(s_baseline)
    return s_baseline
