import pandas as pd
import numpy as np

class MovingAverageCrossover:
    def __init__(self, short_window, long_window):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data):
        """Generate buy/sell signals based on moving average crossover."""
        data['Short_MA'] = data['close'].rolling(window=self.short_window, min_periods=1).mean()
        data['Long_MA'] = data['close'].rolling(window=self.long_window, min_periods=1).mean()
        data['Signal'] = 0
        data['Signal'][self.short_window:] = np.where(
            data['Short_MA'][self.short_window:] > data['Long_MA'][self.short_window:], 1, 0
        )
        data['Position'] = data['Signal'].diff()
        return data