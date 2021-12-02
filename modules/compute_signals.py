## From regression to signal

def get_signal_from_reg(df_test, model, alpha):
    y_pred = model.predict(df_test)

    close_t = df_test['Y_t']
    close_lag_1 = df_test['Y_lag_1']

    signal = []

    for i, pred in enumerate(y_pred):
        #print('\nTime', str(i))
        #print('pred', y_pred.iloc[i] > (1+alpha)*close_lag_1.iloc[i])

        if y_pred.iloc[i] >= (1+alpha)*close_lag_1.iloc[i]:
            #print('pred', y_pred.iloc[i], 'y_{t-1}', close_lag_1.iloc[i])
            #print('long')
            signal.append(1)

        elif y_pred.iloc[i] <= (1-alpha)*close_lag_1.iloc[i]:
            #print('pred', y_pred.iloc[i], 'y_{t-1}', close_lag_1.iloc[i])
            #print('short')
            signal.append(-1)

        else:
            #print('pred', y_pred.iloc[i], 'y_{t-1}', close_lag_1.iloc[i])
            #print('neutral')
            signal.append(0)

    return signal

signal = get_signal_from_reg(df_test, model)
signal = pd.DataFrame(signal)
