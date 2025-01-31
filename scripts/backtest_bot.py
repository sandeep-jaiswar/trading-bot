from core.backtest import Backtest
from logs.logger import get_logger

logger = get_logger(__name__)

def main():
    logger.info("Starting backtesting...")
    backtester = Backtest()
    results = backtester.run_backtest()
    logger.info(f"Backtest results: {results}")

if __name__ == "__main__":
    main()
