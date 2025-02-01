import pandas as pd

class DataPreprocessor:
    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """Clean market data and handle missing values."""
        df.dropna(inplace=True)
        df = df.sort_values(by="timestamp")
        return df

    @staticmethod
    def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
        """Calculate simple moving averages (SMA)."""
        df["SMA_9"] = df["close"].rolling(window=9).mean()
        df["SMA_21"] = df["close"].rolling(window=21).mean()
        return df