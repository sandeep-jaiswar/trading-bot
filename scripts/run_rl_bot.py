from core.order_manager import OrderManager
from ml.reinforcement_learning import predict_trade
from core.risk_management import RiskManagement
from logs.logger import get_logger
import pandas as pd

logger = get_logger(__name__)

def main():
    manager = OrderManager()
    risk = RiskManagement()

    logger.info("Starting Reinforcement Learning Trading Bot...")

    while True:
        df = pd.read_csv("data/historical_data.csv")
        action = predict_trade(df)
        current_price = df["close"].iloc[-1]

        if action == 1:  # Buy
            manager.execute_trade("BTCUSDT", "BUY", "MARKET", 0.001)
            logger.info(f"📈 RL Model recommends buying at {current_price}")
        elif action == 2:  # Sell
            manager.execute_trade("BTCUSDT", "SELL", "MARKET", 0.001)
            logger.info(f"📉 RL Model recommends selling at {current_price}")

        # Check risk management
        if risk.check_drawdown(manager.binance.get_account_balance()["balances"], 10000):
            logger.warning("⚠️ Max drawdown reached. Stopping bot.")
            break

if __name__ == "__main__":
    main()
