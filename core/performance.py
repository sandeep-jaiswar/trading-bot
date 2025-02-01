import numpy as np

class PerformanceMetrics:
    @staticmethod
    def calculate_returns(data):
        """Calculate cumulative returns."""
        data['Returns'] = data['close'].pct_change()
        data['Cumulative_Returns'] = (1 + data['Returns']).cumprod()
        return data

    @staticmethod
    def calculate_drawdown(data):
        """Calculate maximum drawdown."""
        data['Peak'] = data['Cumulative_Returns'].cummax()
        data['Drawdown'] = (data['Cumulative_Returns'] - data['Peak']) / data['Peak']
        return data

    @staticmethod
    def calculate_sharpe_ratio(data, risk_free_rate=0.0):
        """Calculate Sharpe ratio."""
        excess_returns = data['Returns'] - risk_free_rate
        sharpe_ratio = np.sqrt(252) * (excess_returns.mean() / excess_returns.std())
        return sharpe_ratio