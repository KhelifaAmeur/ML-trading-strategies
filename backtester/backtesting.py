## Backtester
import numpy as np
import matplotlib.pyplot as plt

class Position:
    
    def __init__(self):
        self.side = None
        self.entry_price = None
        self.exit_price = None
        self.entry_time = None
        self.exit_time = None
    
    def open_position(self, side, entry_price, entry_time):
        self.side = side
        self.entry_price = entry_price
        self.entry_time = entry_time
    
    def close_position(self, exit_price, exit_time):
        self.exit_price = exit_price
        self.exit_time = exit_time
        
        
class Strategy:
    
    def __init__(self, cash, fees):
        self.fees = fees
        self.tokens = [0]
        self.cash = [cash]
        self.wallet = [cash]
        
        self.positions = [0]
        self.trades = []
        self.verbose = False
        
        self.current_position = None
        
        self.close = None
        self.signals = None

        self.dic_positions = {1:'long', -1:'short'}
    
    def run(self, signals, close, verbose=False):
        self.verbose = verbose
        self.signals = signals
        self.close  = close
        
        for i, s in enumerate(self.signals):
            p = self.positions[i]
            
            if p == 0:
                if self.verbose:
                    print("\n(" + str(i) + ") not in position ")
                if s != 0:
                    self.take_position(i, s, False)
                elif s == 0:
                    self.neutral(i, s, p)
                    
            elif p == 1:
                if self.verbose:
                    print("\n(" + str(i) + ") in position long ")
                if s == 1:
                    self.neutral(i, s, p)
                elif s == 0:
                    self.sell_position(i, p, False)
                elif s == -1:
                    self.sell_position(i, p, True)
                    self.take_position(i, s, True)
            
            elif p == -1:
                if self.verbose:
                    print("\n(" + str(i) + ") in position short ")
                if s == -1:
                    self.neutral(i, s, p)
                elif s == 0:
                    self.sell_position(i, p, False)
                elif s == 1:
                    self.sell_position(i, p, True)
                    self.take_position(i, s, True)
            
            self.wallet.append(self.cash[i]+self.tokens[i]*self.close[i])
            
            if self.verbose:
                print("close", self.close[i])
                print("cash", self.cash[i])
                print("tokens", self.tokens[i])

    
    def take_position(self, i, side, double_order):
        if self.verbose:
            print('enter ' + self.dic_positions[side])
        
        if double_order:
            self.tokens.append((1-2*self.fees)*self.tokens[i])
        if not double_order:
            self.tokens.append(self.cash[i]*(1-self.fees)/self.close[i])
        self.cash.append(0)
        self.positions.append(side)
            
        self.current_position = Position()
        self.current_position.open_position(side=side, entry_price=self.close[i], entry_time=self.signals.index[i])
        

        
    def neutral(self, i, side, position):
        if self.verbose:
            if position == 1 and side == 1:
                print('remain long')
            elif position == -1 and side == -1:
                print('remain short')
            else:
                print("stay neutral")
            
        self.tokens.append(self.tokens[i])
        self.cash.append(self.cash[i])
        self.positions.append(self.positions[i])
        

    def sell_position(self, i, position, double_order):
            
        ROI = position *(self.close[i] - self.current_position.entry_price)/self.current_position.entry_price
        
        if not double_order:
            self.tokens.append(0)
            self.cash.append((1-self.fees) * self.tokens[i] * self.current_position.entry_price * (1 + ROI))   
            self.positions.append(0)
        
        self.current_position.close_position(exit_price=self.close[i], exit_time=self.signals.index[i])
        self.trades.append(self.current_position)
        
        if self.verbose:
            print("exit " + self.dic_positions[position] + " position")
            print("ROI", ROI)
            
    def visualize(self):
        long_prices = []
        short_prices = []
        exit_prices = []
        long_times = []
        short_times = []
        exit_times = []
        
        for trade in self.trades:
            if trade.side == 1:
                long_prices.append(trade.entry_price)
                long_times.append(trade.entry_time)
            elif trade.side == -1:
                short_prices.append(trade.entry_price)
                short_times.append(trade.entry_time)
            
            exit_prices.append(trade.entry_price)
            exit_times.append(trade.exit_time)
        
        fig, axs = plt.subplots(3, 1, figsize=(10,10))
        
        axs[0].plot(self.close.index, self.close, label='Close price')
        axs[0].scatter(long_times, np.array(long_prices)-100, label='Long', color = 'green', marker="^")
        axs[0].scatter(short_times, np.array(short_prices)+100, label='Short', color = 'red', marker="v")
        axs[0].scatter(exit_times, exit_prices, label='Exit', color = 'yellow')
        
        axs[1].plot(self.close.index, self.positions[1:], label='positions', color='black')
        
        axs[2].plot(self.close.index, self.wallet[1:], label='Wallet')
        axs[2].scatter(long_times, np.array(self.wallet[1:])[long_times]-1, label='Long', color = 'green', marker="^")
        axs[2].scatter(short_times, np.array(self.wallet[1:])[short_times]+1, label='Short', color = 'red', marker="v")
        axs[2].scatter(exit_times, np.array(self.wallet[1:])[exit_times], label='Exit', color = 'yellow')
        
        axs[0].legend()
        axs[1].legend()
        axs[2].legend()
        
        plt.tight_layout()
        plt.show()

########################################################
        
        
'''        
def strat(signals, close, verbose=False):
    fees = 0.001
    tokens = [0]
    cash = [500]
    wallet = [500]

    positions = [0]


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
            
        # current_position = Position()
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
        

    def close_position(i, position, double_order):
        
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
            if s != 0:
                take_position(i, s, False)
            elif s == 0:
                neutral(i, s, p)
                
        elif p == 1:
            if verbose:
                print("\n(" + str(i) + ") in position long ")
            if s == 1:
                neutral(i, s, p)
            elif s == 0:
                close_position(i, p, False)
            elif s == -1:
                close_position(i, p, True)
                take_position(i, s, True)
        
        elif p == -1:
            if verbose:
                print("\n(" + str(i) + ") in position short ")
            if s == -1:
                neutral(i, s, p)
            elif s == 0:
                close_position(i, p, False)
            elif s == 1:
                close_position(i, p, True)
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

    return tokens, cash, positions, trades, wallet
'''