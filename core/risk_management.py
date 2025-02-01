from config.config import settings
import yaml

class RiskManagement:
    def __init__(self):
        self.settings = self.load_settings()
        self.max_drawdown = settings["trading"]["max_drawdown"]
        self.stop_loss = settings["trading"]["stop_loss"]
        self.take_profit = settings["trading"]["take_profit"]

    @staticmethod
    def load_settings() -> dict:
        """Load settings from a YAML configuration file."""
        try:
            with open("config/settings.yaml", "r") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise Exception("Configuration file not found.")
        except yaml.YAMLError as e:
            raise Exception(f"Error loading YAML configuration: {e}")

    def check_drawdown(self, balance, initial_balance):
        """Check if drawdown limit is breached."""
        drawdown = ((initial_balance - balance) / initial_balance) * 100
        if drawdown >= self.max_drawdown:
            print(f"🚨 Max drawdown reached: {drawdown:.2f}%. Stopping trading.")
            return True
        return False

    def check_stop_loss(self, entry_price, current_price):
        """Check if stop-loss should be triggered."""
        loss = ((entry_price - current_price) / entry_price) * 100
        return loss <= -self.stop_loss  # Negative because it's a loss

    def check_take_profit(self, entry_price, current_price):
        """Check if take-profit should be triggered."""
        profit = ((current_price - entry_price) / entry_price) * 100
        return profit >= self.take_profit

# Example usage:
# risk = RiskManagement()
# if risk.check_stop_loss(50000, 49000):
#     print("Stop-loss triggered!")
