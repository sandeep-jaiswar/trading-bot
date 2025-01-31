from core.exchange import BinanceAPI

class OrderManager:
    def __init__(self):
        self.binance = BinanceAPI()

    def execute_trade(self, symbol, side, order_type, quantity, price=None):
        """Execute a trade order."""
        try:
            order = self.binance.place_order(symbol, side, order_type, quantity, price)
            if "orderId" in order:
                print(f"Order placed successfully: {order}")
                return order
            else:
                print(f"Order failed: {order}")
        except Exception as e:
            print(f"Error executing trade: {e}")
        return None

# Example usage:
# manager = OrderManager()
# manager.execute_trade("BTCUSDT", "BUY", "MARKET", 0.001)
