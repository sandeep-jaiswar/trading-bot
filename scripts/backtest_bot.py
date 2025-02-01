from logs.logger import get_logger
from core.backtest import Backtester

logger = get_logger(__name__)

def main():
    logger.info("Starting backtesting...")
    symbol = 'BTCUSDT'
    interval = '1d'
    start_date = '2022-01-01'
    short_window = 10
    long_window = 50
    initial_capital = 10000
    backtester = Backtester(symbol, interval, start_date, short_window, long_window, initial_capital)
    results = backtester.run_backtest()
    logger.info(f"Backtest results: {results}")

if __name__ == "__main__":
    main()
