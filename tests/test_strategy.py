import unittest
from core.strategy import Strategy

class TestStrategy(unittest.TestCase):
    def setUp(self):
        self.strategy = Strategy()

    def test_moving_average_crossover(self):
        signal = self.strategy.moving_average_crossover()
        self.assertIn(signal, ["BUY", "SELL", "HOLD"])

if __name__ == "__main__":
    unittest.main()
