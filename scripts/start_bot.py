from core.order_manager import OrderManager
from core.strategy import Strategy
from logs.logger import get_logger

logger = get_logger(__name__)

def main():
    strategy = Strategy()
    manager = OrderManager()

    logger.info("Starting trading bot...")

    while True:
        signal = strategy.moving_average_crossover()
        
        if signal == "BUY":
            manager.execute_trade("BTCUSDT", "BUY", "MARKET", 0.001)
        elif signal == "SELL":
            manager.execute_trade("BTCUSDT", "SELL", "MARKET", 0.001)

if __name__ == "__main__":
    main()
