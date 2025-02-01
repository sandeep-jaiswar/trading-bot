from core.order_manager import OrderManager
from ml.model import TradePredictor
from core.risk_management import RiskManagement
from logs.logger import get_logger

logger = get_logger(__name__)

def main():
    predictor = TradePredictor()
    manager = OrderManager()
    risk = RiskManagement()

    logger.info("Starting ML-powered trading bot...")

    while True:
        df = predictor.load_data()[0]  # Get latest market data
        signal = predictor.predict_signal(df)

        entry_price = df["close"].iloc[-1]

        if signal == "BUY":
            manager.execute_trade("BTCUSDT", "BUY", "MARKET", 0.001)
            logger.info(f"📈 Buy order placed at {entry_price}")
        elif signal == "SELL":
            manager.execute_trade("BTCUSDT", "SELL", "MARKET", 0.001)
            logger.info(f"📉 Sell order placed at {entry_price}")

        # Check risk management
        if risk.check_drawdown(manager.binance.get_account_balance()["balances"], 10000):  # Example initial balance
            logger.warning("⚠️ Max drawdown reached. Stopping bot.")
            break

if __name__ == "__main__":
    main()
