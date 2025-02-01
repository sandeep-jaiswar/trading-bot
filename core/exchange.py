import os
import time
import hmac
import hashlib
import pandas as pd
import requests
import websocket
import threading
import json
from urllib.parse import urlencode
from config.config import Config
from typing import Callable, Dict, Any
from binance.client import Client

class BinanceAPI:
    def __init__(self):
        self.client = Client(Config.BINANCE_API_KEY, Config.BINANCE_SECRET_KEY)
        self.base_url = "https://testnet.binance.vision" if Config.TESTNET else Config.BASE_URL
        self.ws_url = "wss://stream.binance.com:9443/ws"
        self.ws_thread = None
        self.ws = None

    def get_account_balance(self) -> Dict[str, Any]:
        """Fetch account balance."""
        return self.client.get_account()

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> Dict[str, Any]:
        """Place a market or limit order."""
        return self.client.create_order(
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=quantity,
            price=price
        )

    def get_historical_klines(self, symbol: str, interval: str, start_time: int = None, end_time: int = None) -> Dict[str, Any]:
        """Fetch historical candlestick data from Binance."""
        klines = self.client.get_historical_klines(
            symbol=symbol,
            interval=interval,
            start_str=start_time,
            end_str=end_time
        )
        data = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
            'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
            'taker_buy_quote_asset_volume', 'ignore'
        ])
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
        data['close'] = data['close'].astype(float)
        return data

    def get_symbol_ticker(self, symbol: str) -> Dict[str, Any]:
        """Fetch the latest price for a symbol."""
        return self.client.get_symbol_ticker(symbol=symbol)

    def start_websocket(self, symbol: str, on_message_callback: Callable[[Dict[str, Any]], None]) -> websocket.WebSocketApp:
        """Start WebSocket connection for live market data."""
        url = f"{self.ws_url}/{symbol.lower()}@kline_1m"

        def on_message(ws, message):
            """Handle incoming WebSocket messages."""
            data = json.loads(message)
            on_message_callback(data)

        self.ws = websocket.WebSocketApp(url, on_message=on_message)
        self.ws_thread = threading.Thread(target=self.ws.run_forever)
        self.ws_thread.daemon = True
        self.ws_thread.start()
        return self.ws

    def stop_websocket(self):
        """Stop the WebSocket connection."""
        if self.ws:
            self.ws.close()
            self.ws_thread.join()

# Example usage:
# binance = BinanceAPI()
# print(binance.get_account_balance())