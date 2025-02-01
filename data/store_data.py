import pandas as pd
from database.database import create_table, insert_data

class DataStorage:
    def __init__(self):
        # You can initialize any necessary parameters here if needed
        pass

    def store_data(self, df: pd.DataFrame) -> None:
        """Store market data to the database."""
        try:
            create_table()  # Ensure the table exists
            insert_data(df)  # Insert the data
        except Exception as e:
            print(f"Error storing data: {e}")