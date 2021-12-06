#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 16:09:50 2021

@author: stanislasbucaille
"""
import pandas as pd
from keras.layers import Dense
from keras import Input, Model

class Autoencoder:
    
    def __init__(self, input_size):
        self.n = input_size
        self.autoencoder = None
        self.encoder = None
    
    def build_model(self):
        input_img = Input(shape=(self.n,))

        # encodeding
        encodeding_1 = Dense(50, activation='relu')(input_img)
        encodeding_2 = Dense(25, activation='relu')(encodeding_1)
        encoded = Dense(5, activation='relu')(encodeding_2)

        # decodeding
        decodeding_1 = Dense(25, activation='sigmoid')(encoded)
        decodeding_2 = Dense(50, activation='sigmoid')(decodeding_1)
        decoded = Dense(self.n, activation='sigmoid')(decodeding_2)

        # Autoencoder - model
        self.autoencoder = Model(input_img, decoded)

        # Encoder - model
        self.encoder = Model(input_img, encoded)
        
    
    def train(self, df):
        m, n = df.shape
        val_split = int(n*0.8)
        
        df_train = df[:-val_split]
        df_val = df[-val_split:]
        
        self.autoencoder.compile(optimizer='adam', loss='mean_squared_error')
        self.autoencoder.fit(df_train, df_train, 
                             epochs=5, batch_size=10, 
                             validation_data=(df_val, df_val))
        
    def encode(self, df):
        col_names = [f'dw_latent_{i}' for i in range(5)]
        df_encoded = self.encoder.predict(df)
        
        df_encoded = pd.DataFrame(df_encoded, columns=col_names)
        return df_encoded