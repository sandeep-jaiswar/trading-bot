import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
import pickle

class LSTMPredictor:
    def __init__(self, time_steps=60):
        self.model = self._build_model()
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.time_steps = time_steps

    def _build_model(self):
        """Build an LSTM model for time-series forecasting."""
        model = Sequential([
            LSTM(units=50, return_sequences=True, input_shape=(self.time_steps, 1)),
            Dropout(0.2),
            LSTM(units=50, return_sequences=True),
            Dropout(0.2),
            LSTM(units=50),
            Dropout(0.2),
            Dense(units=1)
        ])
        model.compile(optimizer="adam", loss="mean_squared_error")
        return model

    def train_model(self, df):
        """Train the LSTM model on historical market data."""
        df["close"] = self.scaler.fit_transform(df["close"].values.reshape(-1, 1))

        X, y = [], []
        for i in range(self.time_steps, len(df)):
            X.append(df["close"].iloc[i-self.time_steps:i].values)
            y.append(df["close"].iloc[i])

        X, y = np.array(X), np.array(y)
        X = X.reshape((X.shape[0], X.shape[1], 1))

        self.model.fit(X, y, epochs=50, batch_size=32, verbose=1)

        # Save model & scaler
        self.model.save("ml/lstm_model.h5")
        with open("ml/scaler.pkl", "wb") as f:
            pickle.dump(self.scaler, f)

    def predict_price(self, df):
        """Predict the next price movement."""
        with open("ml/scaler.pkl", "rb") as f:
            self.scaler = pickle.load(f)

        latest_data = df["close"].iloc[-self.time_steps:].values.reshape(-1, 1)
        latest_data = self.scaler.transform(latest_data)
        latest_data = latest_data.reshape((1, self.time_steps, 1))

        prediction = self.model.predict(latest_data)
        return self.scaler.inverse_transform(prediction)[0, 0]

# Example Usage:
# predictor = LSTMPredictor()
# predictor.train_model(historical_df)
