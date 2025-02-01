from core.exchange import BinanceAPI
import pandas as pd
from database import insert_data, create_table
from datetime import datetime

def fetch_binance_data(symbol: str, interval: str, lookback: str = "1 day ago UTC") -> pd.DataFrame:
    """Fetch market data from Binance and return as a DataFrame.

    Args:
        symbol (str): The trading pair symbol (e.g., 'BTCUSDT').
        interval (str): The time interval for the candlestick data (e.g., '1m').
        lookback (str): The lookback period for fetching data (default is '1 day ago UTC').

    Returns:
        pd.DataFrame: A DataFrame containing the fetched market data.
    """
    try:
        client = BinanceAPI()
        print(f"Fetching data for {symbol} ({interval})...")
        print(f"Lookback period: {lookback}")
        print("=====================================")
        # Convert lookback period to Unix timestamp
        # lookback_unix = pd.to_datetime(lookback).timestamp() * 1000
        start_time = int(datetime(2023, 1, 1).timestamp() * 1000)  # Start time in milliseconds (e.g., Jan 1, 2023)
        end_time = int(datetime(2023, 1, 10).timestamp() * 1000)    # End time in milliseconds (e.g., Jan 10, 2023)
        candles = client.get_historical_klines(symbol, interval, start_time=start_time, end_time=end_time)
    except Exception as e:
        print(f"Error fetching data from Binance: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

    # Convert to DataFrame and keep only the relevant columns
    df = pd.DataFrame(candles, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    
    # Convert data types
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
    
    # Keep only the relevant columns
    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    
    # Insert data into PostgreSQL
    try:
        create_table()
        insert_data(df)
    except Exception as e:
        print(f"Error inserting data into database: {e}")

    return df