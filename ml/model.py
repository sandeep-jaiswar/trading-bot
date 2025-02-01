import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle

class TradePredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()

    def load_data(self, file_path="data/historical_data.csv"):
        """Load historical market data."""
        df = pd.read_csv(file_path)
        df["SMA_9"] = df["close"].rolling(window=9).mean()
        df["SMA_21"] = df["close"].rolling(window=21).mean()
        df.dropna(inplace=True)

        df["target"] = np.where(df["SMA_9"] > df["SMA_21"], 1, 0)  # 1 = BUY, 0 = SELL

        X = df[["SMA_9", "SMA_21", "close", "volume"]]
        y = df["target"]

        return train_test_split(X, y, test_size=0.2, random_state=42)

    def train_model(self):
        """Train the ML model."""
        X_train, X_test, y_train, y_test = self.load_data()
        self.scaler.fit(X_train)
        X_train_scaled = self.scaler.transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        self.model.fit(X_train_scaled, y_train)
        accuracy = self.model.score(X_test_scaled, y_test)
        print(f"Model accuracy: {accuracy:.2f}")

        # Save model
        with open("ml/trade_model.pkl", "wb") as f:
            pickle.dump((self.model, self.scaler), f)

    def predict_signal(self, df):
        """Predict trade signal using ML model."""
        with open("ml/trade_model.pkl", "rb") as f:
            self.model, self.scaler = pickle.load(f)

        X = df[["SMA_9", "SMA_21", "close", "volume"]].tail(1)
        X_scaled = self.scaler.transform(X)

        return "BUY" if self.model.predict(X_scaled)[0] == 1 else "SELL"

# Example usage:
# predictor = TradePredictor()
# predictor.train_model()
