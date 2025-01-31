import psycopg2
from config.config import settings
import pandas as pd

class DataStorage:
    def __init__(self):
        self.db_params = {
            "dbname": "trading_bot",
            "user": "postgres",
            "password": "your_password",
            "host": "localhost",
            "port": "5432"
        }
        self.conn = psycopg2.connect(**self.db_params)
        self.cursor = self.conn.cursor()

    def create_table(self):
        """Create a table for storing market data."""
        query = """
        CREATE TABLE IF NOT EXISTS market_data (
            timestamp TIMESTAMP PRIMARY KEY,
            open FLOAT,
            high FLOAT,
            low FLOAT,
            close FLOAT,
            volume FLOAT
        );
        """
        self.cursor.execute(query)
        self.conn.commit()

    def save_data(self, df: pd.DataFrame):
        """Save market data to the database."""
        for _, row in df.iterrows():
            query = """
            INSERT INTO market_data (timestamp, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (timestamp) DO NOTHING;
            """
            self.cursor.execute(query, tuple(row))
        self.conn.commit()

# Example usage:
# storage = DataStorage()
# storage.create_table()
# storage.save_data(df)
