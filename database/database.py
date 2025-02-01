import os
import psycopg2
from psycopg2 import sql
import pandas as pd
from indicators.technical_indicators import TechnicalIndicators 

def get_db_connection() -> psycopg2.extensions.connection:
    """Connect to PostgreSQL database"""
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )
    return conn

def create_table() -> None:
    """Create a table to store Binance market data"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(""" 
                    CREATE TABLE IF NOT EXISTS market_data (
                        timestamp TIMESTAMPTZ PRIMARY KEY,
                        open DOUBLE PRECISION,
                        high DOUBLE PRECISION,
                        low DOUBLE PRECISION,
                        close DOUBLE PRECISION,
                        volume DOUBLE PRECISION
                    );
                """)
                conn.commit()
    except Exception as e:
        print(f"Error creating table: {e}")

def insert_data(df: pd.DataFrame) -> None:
    """Insert fetched data into PostgreSQL table"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Prepare the insert statement
                insert_query = """
                    INSERT INTO market_data (timestamp, open, high, low, close, volume)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (timestamp) DO NOTHING;
                """
                # Use executemany for batch insertion
                cursor.executemany(insert_query, [
                    (row['timestamp'], row['open'], row['high'], row['low'], row['close'], row['volume'])
                    for index, row in df.iterrows()
                ])
                conn.commit()
    except Exception as e:
        print(f"Error inserting data: {e}")


def fetch_data_from_db():
    """Fetch market data from PostgreSQL"""
    conn = get_db_connection()
    query = "SELECT * FROM market_data ORDER BY timestamp ASC;"
    df = pd.read_sql(query, conn)
    df = TechnicalIndicators.calculate_rsi(df)
    df = TechnicalIndicators.calculate_macd(df)
    df = TechnicalIndicators.calculate_bollinger_bands(df)
    conn.close()
    
    return df