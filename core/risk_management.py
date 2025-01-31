from config.config import settings

class RiskManagement:
    def __init__(self):
        self.max_drawdown = settings["trading"]["max_drawdown"]

    def check_drawdown(self, balance, initial_balance):
        """Check if drawdown limit is breached."""
        drawdown = ((initial_balance - balance) / initial_balance) * 100
        if drawdown >= self.max_drawdown:
            print(f"Max drawdown reached: {drawdown:.2f}%. Stopping trading.")
            return True
        return False

# Example usage:
# risk = RiskManagement()
# if risk.check_drawdown(current_balance, starting_balance):
#     stop_trading()
