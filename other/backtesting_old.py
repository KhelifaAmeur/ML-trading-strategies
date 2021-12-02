## Backtester

def strat(signals, close, verbose=False):
    fees = 0.001
    tokens = [0]
    cash = [500]
    wallet = [500]

    positions = [0]
    long_times = []
    short_times = []
    exit_times = []
    longs = []
    shorts = []
    exits = []

    current_position = {
        "side": None,
        #"qty": 1,
        #"take_profit": 0.5,
        #"stop_loss": -0.2,
        "entry_price": None,
        "exit_price": None,
        "entry_time": None,
        "exit_time": None,
        #"exit_reason": ""
    }
    trades = []

    def enter_long(i):
        tokens.append(cash[i]*(1-fees)/close[i])
        cash.append(0)
        positions.append(1)
        long_times.append(signals.index[i])
        longs.append(close[i])
        # current_postion = Position()
        current_position['side'] = 1
        current_position['entry_price'] = close[i]
        current_position['entry_time'] = signals.index[i]

    def enter_short(i):
        tokens.append(cash[i]*(1-fees)/close[i])
        cash.append(0)
        positions.append(-1)
        short_times.append(signals.index[i])
        shorts.append(close[i])
        current_position['side'] = -1
        current_position['entry_price'] = close[i]
        current_position['entry_time'] = signals.index[i]

    def neutral(i):
        tokens.append(tokens[i])
        cash.append(cash[i])
        positions.append(0)

    def exit(i, why, side, ROI):
        tokens.append(0)
        positions.append(0)
        exit_times.append(signals.index[i])
        exits.append(close[i])

        if side == 1:
            cash.append((1-fees) * tokens[i] * current_position["entry_price"] * (1+ROI/100) )
            current_position['exit_price'] = close[i]
            current_position["exit_time"] = signals.index[i]
            current_position["exit_reason"] = why
            trades.append(current_position.copy())

        if side == -1:
            cash.append((1-fees) * tokens[i] * current_position["entry_price"] * (1+ROI/100) )
            current_position['exit_price'] = close[i]
            current_position["exit_time"] = signals.index[i]
            current_position["exit_reason"] = why
            trades.append(current_position.copy())

    def monitor_exit(i):
        if positions[i] == 1:
            ROI = (close[i] - current_position["entry_price"])*100/current_position["entry_price"]
            if verbose:
                print("ROI", ROI)
            if ROI > 0.5:
                exit(i, "take_profit", 1, ROI)
            elif ROI < -0.2:
                exit(i, "stop_loss", 1, ROI)
            else:
                tokens.append(tokens[i])
                cash.append(cash[i])
                positions.append(1)

        if positions[i] == -1:
            ROI = -(close[i] - current_position["entry_price"])*100/current_position["entry_price"]
            if verbose:
                print("ROI", ROI)
            if ROI > 0.5:
                exit(i, "take_profit", -1, ROI)
            elif ROI < -0.2:
                exit(i, "stop_loss", -1, ROI)
            else:
                tokens.append(tokens[i])
                cash.append(cash[i])
                positions.append(-1)

    for i, s in enumerate(signals):
        print(i)
        if positions[i] == 0:
            if verbose:
                print("\nnot in position, " + str(i))
            # long signal, enter long
            if s == 1:
                if verbose:
                    print("enter long")
                enter_long(i)

            # short signal, enter short
            if s == -1:
                if verbose:
                    print("enter short")
                enter_short(i)

            # stay neutral
            if s == 0:
                if verbose:
                    print("stay neutral")
                neutral(i)

        if positions[i] != 0 :
            if verbose:
                print("\nin position, " + str(i))
                print(current_position)
            # monitor return
            monitor_exit(i)

        if verbose:
            print("close", close[i])
            print("cash", cash[i])
            print("tokens", tokens[i])

    return tokens, cash, positions, long_times, short_times, exit_times, longs, shorts, exits, trades