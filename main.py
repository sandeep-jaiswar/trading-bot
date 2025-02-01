import pandas as pd
from core.order_manager import OrderManager
from database.database import get_db_connection
from ml.deep_learning_model import LSTMPredictor
from ml.reinforcement_learning import train_rl_agent, predict_trade
from indicators.technical_indicators import TechnicalIndicators
from core.risk_management import RiskManagement
from logs.logger import get_logger
import time
from binance_data_fetcher import fetch_binance_data
from database.database import fetch_data_from_db

logger = get_logger(__name__)

def main():
    fetch_binance_data("BTCUSDT", "1h")
    logger.info("Starting the Trading Bot...")

    # Load historical data
    df = fetch_data_from_db()

    # Preprocess data (apply technical indicators)
    df = TechnicalIndicators.calculate_rsi(df)
    df = TechnicalIndicators.calculate_macd(df)
    df = TechnicalIndicators.calculate_bollinger_bands(df)

    # Initialize the OrderManager and RiskManagement classes
    manager = OrderManager()
    risk = RiskManagement()

    # Train RL agent (run once)
    logger.info("----------------------------training---------------------------")
    train_rl_agent(df)
    logger.info("----------------------------done traiing---------------------------")

    # Start the trading loop
    while True:
        try:
            # Get the action predicted by the RL model (Buy, Sell, Hold)
            action = predict_trade(df)

            # Get current market price
            current_price = df["close"].iloc[-1]

            if action == 1:  # Buy
                manager.execute_trade("BTCUSDT", "BUY", "MARKET", 0.001)
                logger.info(f"📈 RL Model recommends buying at {current_price}")
            elif action == 2:  # Sell
                manager.execute_trade("BTCUSDT", "SELL", "MARKET", 0.001)
                logger.info(f"📉 RL Model recommends selling at {current_price}")

            # Check risk management (for drawdowns)
            if risk.check_drawdown(manager.binance.get_account_balance()["balances"], 10000):
                logger.warning("⚠️ Max drawdown reached. Stopping bot.")
                break

            # Sleep to simulate trading every X seconds/minutes
            time.sleep(60)  # Adjust this based on your time-frame for trading

        except Exception as e:
            logger.error(f"Error during trading loop: {e}")
            break

if __name__ == "__main__":
    main()
