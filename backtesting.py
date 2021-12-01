## Backtester
'''
class Strategy:
    
    def __init__(self, ):
        self.fees = 0.001
        self.tokens = [0]
        self.cash = [500]
        self.wallet = [500]
        
        self.positions = [0]
        self.long_times = []
        self.short_times = []
        self.exit_times = []
        self.
        self.
        self.
'''   
########################################################
        
        
        
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
        "entry_price": None,
        "exit_price": None,
        "entry_time": None,
        "exit_time": None,
    }
    trades = []


    def take_position(i, side, double_order):
        if verbose:
            print('enter ' + dic_positions[side])
        
        if double_order:
            tokens.append((1-2*fees)*tokens[i])
        if not double_order:
            tokens.append(cash[i]*(1-fees)/close[i])
            
        cash.append(0)
        positions.append(side)
        
        if side == 1:
            long_times.append(signals.index[i])
            longs.append(close[i])
        elif side == -1:  
            short_times.append(signals.index[i])
            shorts.append(close[i])
            
        # current_postion = Position()
        current_position['side'] = side
        current_position['entry_price'] = close[i]
        current_position['entry_time'] = signals.index[i]  
        
    def neutral(i, side, position):
        if verbose:
            if position == 1 and side == 1:
                print('remain long')
            elif position == -1 and side == -1:
                print('remain short')
            else:
                print("stay neutral")
            
        tokens.append(tokens[i])
        cash.append(cash[i])
        positions.append(positions[i])
        

    def sell(i, position, double_order):
            
        exit_times.append(signals.index[i])
        exits.append(close[i])
        
        ROI = position *(close[i] - current_position["entry_price"])/current_position["entry_price"]
        
        if not double_order:
            tokens.append(0)
            cash.append((1-fees) * tokens[i] * current_position["entry_price"] * (1 + ROI))   
            positions.append(0)
        
        current_position['exit_price'] = close[i]
        current_position["exit_time"] = signals.index[i]
        trades.append(current_position.copy())
        
        if verbose:
            print("exit " + dic_positions[position] + " position")
            print("ROI", ROI)
        

           

    dic_positions = {1:'long', -1:'short'}

    for i, s in enumerate(signals):
        p = positions[i]
        
        if p == 0:
            if verbose:
                print("\n(" + str(i) + ") not in position ")
            
            # take position
            if s != 0:
                take_position(i, s, False)

            # stay neutral
            elif s == 0:
                neutral(i, s, p)
                
        elif p == 1:
            if verbose:
                print("\n(" + str(i) + ") in position long ")
                
            if s == 1:
                neutral(i, s, p)
            
            elif s == 0:
                sell(i, p, False)

            elif s == -1:
                sell(i, p, True)
                take_position(i, s, True)
        
        elif p == -1:
            if verbose:
                print("\n(" + str(i) + ") in position short ")
                
            if s == -1:
                neutral(i, s, p)
            
            elif s == 0:
                sell(i, p, False)

            elif s == 1:
                sell(i, p, True)
                take_position(i, s, True)
                
        if p == 0:
            wallet.append(wallet[i])
        else:
            ROI = p *(close[i] - current_position["entry_price"])/current_position["entry_price"]
            wallet.append(wallet[i]*(1+ROI))

            
               

        if verbose:
            print("close", close[i])
            print("cash", cash[i])
            print("tokens", tokens[i])

    return tokens, cash, positions, long_times, short_times, exit_times, longs, shorts, exits, trades, wallet