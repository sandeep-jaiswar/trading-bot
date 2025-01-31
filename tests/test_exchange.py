import unittest
from core.exchange import BinanceAPI

class TestBinanceAPI(unittest.TestCase):
    def setUp(self):
        self.binance = BinanceAPI()

    def test_get_account_balance(self):
        balance = self.binance.get_account_balance()
        self.assertIn("balances", balance)

    def test_place_order(self):
        order = self.binance.place_order("BTCUSDT", "BUY", "MARKET", 0.001)
        self.assertIn("orderId", order)  # Expecting order ID in response

if __name__ == "__main__":
    unittest.main()
