import pandas as pd

class TechnicalIndicators:
    @staticmethod
    def calculate_rsi(df, period=14):
        """Calculate Relative Strength Index (RSI)."""
        delta = df["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        df["RSI"] = 100 - (100 / (1 + rs))
        return df

    @staticmethod
    def calculate_macd(df):
        """Calculate MACD (Moving Average Convergence Divergence)."""
        short_ema = df["close"].ewm(span=12, adjust=False).mean()
        long_ema = df["close"].ewm(span=26, adjust=False).mean()
        df["MACD"] = short_ema - long_ema
        df["Signal_Line"] = df["MACD"].ewm(span=9, adjust=False).mean()
        return df

    @staticmethod
    def calculate_bollinger_bands(df, window=20, num_std=2):
        """Calculate Bollinger Bands."""
        df["SMA"] = df["close"].rolling(window=window).mean()
        df["Upper_Band"] = df["SMA"] + (df["close"].rolling(window=window).std() * num_std)
        df["Lower_Band"] = df["SMA"] - (df["close"].rolling(window=window).std() * num_std)
        return df

# Example Usage:
# indicators = TechnicalIndicators()
# df = indicators.calculate_rsi(df)
# df = indicators.calculate_macd(df)
# df = indicators.calculate_bollinger_bands(df)
