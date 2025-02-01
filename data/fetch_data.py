import requests
import pandas as pd
from core.exchange import BinanceAPI
from config.config import settings

class DataFetcher:
    def __init__(self, interval="1m", limit=1000):
        self.binance = BinanceAPI()
        self.symbol = settings["trading"]["symbol"]
        self.interval = interval
        self.limit = limit

    def get_historical_data(self) -> pd.DataFrame:
        """Fetch historical kline (candlestick) data from Binance API."""
        endpoint = "/api/v3/klines"
        params = {
            "symbol": self.symbol,
            "interval": self.interval,
            "limit": self.limit
        }
        try:
            response = requests.get(self.binance.base_url + endpoint, params=params)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return pd.DataFrame()  # Return an empty DataFrame on error

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