import pandas as pd
import numpy as np
import requests
from core.exchange import BinanceAPI
from config.config import settings

class Strategy:
    def __init__(self):
        self.binance = BinanceAPI()
        self.symbol = settings["trading"]["symbol"]
        self.short_window = settings["strategy"]["short_window"]
        self.long_window = settings["strategy"]["long_window"]

    def get_historical_data(self, limit=100):
        """Fetch historical kline data from Binance API."""
        endpoint = "/api/v3/klines"
        params = {
            "symbol": self.symbol,
            "interval": "1m",
            "limit": limit
        }
        response = requests.get(self.binance.base_url + endpoint, params=params)
        data = response.json()
        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])
        df["close"] = df["close"].astype(float)
        return df

    def moving_average_crossover(self):
        """Determine buy/sell signals based on moving averages."""
        df = self.get_historical_data()
        df["short_ma"] = df["close"].rolling(window=self.short_window).mean()
        df["long_ma"] = df["close"].rolling(window=self.long_window).mean()

        if df["short_ma"].iloc[-1] > df["long_ma"].iloc[-1]:
            return "BUY"
        elif df["short_ma"].iloc[-1] < df["long_ma"].iloc[-1]:
            return "SELL"
        return "HOLD"
    
    def bolinger_bands(self):
        """Determine buy/sell signals based on Bollinger Bands."""
        df = self.get_historical_data()
        df["sma"] = df["close"].rolling(window=20).mean()
        df["std"] = df["close"].rolling(window=20).std()
        df["upper_band"] = df["sma"] + (2 * df["std"])
        df["lower_band"] = df["sma"] - (2 * df["std"])

        if df["close"].iloc[-1] < df["lower_band"].iloc[-1]:
            return "BUY"
        elif df["close"].iloc[-1] > df["upper_band"].iloc[-1]:
            return "SELL"
        return "HOLD"
    
    def rsi(self):
        """Determine buy/sell signals based on RSI."""
        df = self.get_historical_data()
        delta = df["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        if rsi.iloc[-1] < 30:
            return "BUY"
        elif rsi.iloc[-1] > 70:
            return "SELL"
        return "HOLD"
    
    def macd(self):
        """Determine buy/sell signals based on MACD."""
        df = self.get_historical_data()
        df["short_ema"] = df["close"].ewm(span=12, adjust=False).mean()
        df["long_ema"] = df["close"].ewm(span=26, adjust=False).mean()
        df["macd"] = df["short_ema"] - df["long_ema"]
        df["signal_line"] = df["macd"].ewm(span=9, adjust=False).mean()

        if df["macd"].iloc[-1] > df["signal_line"].iloc[-1]:
            return "BUY"
        elif df["macd"].iloc[-1] < df["signal_line"].iloc[-1]:
            return "SELL"
        return "HOLD"
    
    def dual_ma_crossover_with_rsi(self):
        """Determine buy/sell signals based on dual MA crossover with RSI."""
        df = self.get_historical_data()
        df["short_ma"] = df["close"].rolling(window=10).mean()
        df["long_ma"] = df["close"].rolling(window=50).mean()
        delta = df["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        if df["short_ma"].iloc[-1] > df["long_ma"].iloc[-1] and rsi.iloc[-1] < 70:
            return "BUY"
        elif df["short_ma"].iloc[-1] < df["long_ma"].iloc[-1] and rsi.iloc[-1] > 30:
            return "SELL"
        return "HOLD"
    
    def mean_reversion(self):
        """Determine buy/sell signals based on mean reversion."""
        df = self.get_historical_data()
        df["mean"] = df["close"].rolling(window=20).mean()
        df["std"] = df["close"].rolling(window=20).std()

        if df["close"].iloc[-1] < (df["mean"].iloc[-1] - 1.0 * df["std"].iloc[-1]):
            return "BUY"
        elif df["close"].iloc[-1] > (df["mean"].iloc[-1] + 1.0 * df["std"].iloc[-1]):
            return "SELL"
        return "HOLD"
    
    def breakout(self):
        """Determine buy/sell signals based on breakout strategy."""
        df = self.get_historical_data()
        df["high"] = df["high"].rolling(window=20).max()
        df["low"] = df["low"].rolling(window=20).min()

        if df["close"].iloc[-1] > df["high"].iloc[-1]:
            return "BUY"
        elif df["close"].iloc[-1] < df["low"].iloc[-1]:
            return "SELL"
        return "HOLD"
