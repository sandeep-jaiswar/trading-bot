from core.order_manager import OrderManager
from ml.deep_learning_model import LSTMPredictor
from indicators.technical_indicators import TechnicalIndicators
from core.risk_management import RiskManagement
from logs.logger import get_logger
import pandas as pd

logger = get_logger(__name__)

def main():
    lstm_predictor = LSTMPredictor()
    manager = OrderManager()
    risk = RiskManagement()

    logger.info("Starting deep learning trading bot...")

    while True:
        df = pd.read_csv("data/historical_data.csv")
        df = TechnicalIndicators.calculate_rsi(df)
        df = TechnicalIndicators.calculate_macd(df)
        df = TechnicalIndicators.calculate_bollinger_bands(df)

        predicted_price = lstm_predictor.predict_price(df)
        current_price = df["close"].iloc[-1]

        if predicted_price > current_price:
            manager.execute_trade("BTCUSDT", "BUY", "MARKET", 0.001)
            logger.info(f"📈 LSTM predicted price increase. Buying at {current_price}")
        elif predicted_price < current_price:
            manager.execute_trade("BTCUSDT", "SELL", "MARKET", 0.001)
            logger.info(f"📉 LSTM predicted price drop. Selling at {current_price}")

        # Check risk management
        if risk.check_drawdown(manager.binance.get_account_balance()["balances"], 10000):
            logger.warning("⚠️ Max drawdown reached. Stopping bot.")
            break

if __name__ == "__main__":
    main()
