import requests
import pandas as pd
from core.exchange import BinanceAPI
from config.config import settings

class DataFetcher:
    def __init__(self):
        self.binance = BinanceAPI()
        self.symbol = settings["trading"]["symbol"]

    def get_historical_data(self, interval="1m", limit=1000):
        """Fetch historical kline (candlestick) data from Binance API."""
        endpoint = "/api/v3/klines"
        params = {
            "symbol": self.symbol,
            "interval": interval,
            "limit": limit
        }
        response = requests.get(self.binance.base_url + endpoint, params=params)
        data = response.json()

        # Convert to DataFrame
        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df["close"] = df["close"].astype(float)
        df["open"] = df["open"].astype(float)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        return df

# Example usage:
# fetcher = DataFetcher()
# df = fetcher.get_historical_data()
# print(df.head())
