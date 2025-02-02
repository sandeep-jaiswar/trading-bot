import pandas as pd
import matplotlib.pyplot as plt
from signals.generator import Generator
from .performance import PerformanceMetrics
from .exchange import BinanceAPI

class Backtester:
    def __init__(self, symbol, interval, start_date, short_window, long_window, initial_capital):
        self.client = BinanceAPI()
        self.strategy = Generator(short_window, long_window)
        self.performance = PerformanceMetrics()
        self.symbol = symbol
        self.interval = interval
        self.start_date = start_date
        self.initial_capital = initial_capital

    def run_backtest(self):
        """Run the backtest."""
        # Fetch historical data
        data = self.client.get_historical_klines(self.symbol, self.interval, self.start_date)

        # Generate signals
        data = self.strategy.generate_signals(data)

        # Calculate performance metrics
        data = self.performance.calculate_returns(data)
        data = self.performance.calculate_drawdown(data)
        sharpe_ratio = self.performance.calculate_sharpe_ratio(data)

        # Simulate trades
        portfolio = self.simulate_trades(data)

        # Plot results
        self.plot_results(data, portfolio)

        # Print performance metrics
        print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
        print(f"Final Portfolio Value: ${portfolio['Total'].iloc[-1]:.2f}")

    def simulate_trades(self, data):
        """Simulate trades based on signals."""
        position = 0
        capital = self.initial_capital
        portfolio = pd.DataFrame(index=data['timestamp'])
        portfolio['Holdings'] = 0.0
        portfolio['Cash'] = self.initial_capital
        portfolio['Total'] = self.initial_capital

        for i, row in data.iterrows():
            capital = int(capital)
            close_price = int(row['close'])
            if row['Position'] == 1:
                print(f"Buying {capital / close_price} shares at ${close_price}")
                position += capital / close_price
                capital -= position * close_price
                print(f"Position: {position}, Capital: {capital}")
            elif row['Position'] == -1:
                print(f"Selling {position} shares at ${close_price}")
                capital += position * close_price
                position = 0
                print(f"Position: {position}, Capital: {capital}")

            portfolio.loc[i, 'Holdings'] = position * close_price
            portfolio.loc[i, 'Cash'] = capital
            portfolio.loc[i, 'Total'] = portfolio.loc[i, 'Holdings'] + portfolio.loc[i, 'Cash']

        return portfolio

    def plot_results(self, data, portfolio):
        """Plot backtest results."""
        plt.figure(figsize=(14, 7))
        plt.plot(data['timestamp'], data['close'], label='Price')
        plt.plot(data['timestamp'], data['Short_MA'], label=f'{self.strategy.short_window}-Day MA')
        plt.plot(data['timestamp'], data['Long_MA'], label=f'{self.strategy.long_window}-Day MA')
        plt.plot(data[data['Position'] == 1]['timestamp'], data['Short_MA'][data['Position'] == 1], '^', markersize=10, color='g', lw=0, label='Buy Signal')
        plt.plot(data[data['Position'] == -1]['timestamp'], data['Short_MA'][data['Position'] == -1], 'v', markersize=10, color='r', lw=0, label='Sell Signal')
        plt.title(f'{self.symbol} Moving Average Crossover Strategy')
        plt.legend()
        plt.show()

        plt.figure(figsize=(14, 7))
        plt.plot(portfolio['Total'], label='Portfolio Value')
        plt.title('Portfolio Performance')
        plt.legend()
        plt.show()