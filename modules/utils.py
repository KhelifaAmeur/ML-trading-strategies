#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 20:18:17 2021

@author: stanislasbucaille
"""
import numpy as np
import random as rd
import pandas as pd


def crop_window(data, nb_days):
    nb_hours = 24*nb_days
    rd_start = rd.randint(0, data.shape[0] - nb_hours)
    data_crop = data[rd_start: rd_start + nb_hours].reset_index(drop=True)
    return data_crop



def array_to_df(arr, columns):
    df = pd.DataFrame(arr, columns=columns)
    return df