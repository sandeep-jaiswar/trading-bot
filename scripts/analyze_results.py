import pandas as pd

def analyze_performance(log_file="logs/trading_bot.log"):
    """Analyze trading bot logs for performance insights."""
    with open(log_file, "r") as file:
        logs = file.readlines()

    trades = [line for line in logs if "Order placed successfully" in line]
    print(f"Total Trades Executed: {len(trades)}")

if __name__ == "__main__":
    analyze_performance()
