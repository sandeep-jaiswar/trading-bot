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

# Example usage:
# strategy = Strategy()
# print(strategy.moving_average_crossover())
