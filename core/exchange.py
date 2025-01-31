import os
import time
import hmac
import hashlib
import requests
import websocket
import threading
import json
from urllib.parse import urlencode
from config.config import Config

class BinanceAPI:
    def __init__(self):
        self.api_key = Config.BINANCE_API_KEY
        self.secret_key = Config.BINANCE_SECRET_KEY
        self.base_url = "https://testnet.binance.vision" if Config.TESTNET else Config.BASE_URL
        self.ws_url = "wss://stream.binance.com:9443/ws"
    
    def _generate_signature(self, params):
        """Generate HMAC SHA256 signature."""
        query_string = urlencode(params)
        return hmac.new(self.secret_key.encode(), query_string.encode(), hashlib.sha256).hexdigest()

    def get_account_balance(self):
        """Fetch account balance."""
        endpoint = "/api/v3/account"
        timestamp = int(time.time() * 1000)
        params = {"timestamp": timestamp}
        params["signature"] = self._generate_signature(params)
        
        headers = {"X-MBX-APIKEY": self.api_key}
        response = requests.get(self.base_url + endpoint, params=params, headers=headers)
        return response.json()
    
    def place_order(self, symbol, side, order_type, quantity, price=None):
        """Place a market or limit order."""
        endpoint = "/api/v3/order"
        timestamp = int(time.time() * 1000)
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
            "timestamp": timestamp,
        }
        if order_type == "LIMIT":
            params.update({"timeInForce": "GTC", "price": price})

        params["signature"] = self._generate_signature(params)
        headers = {"X-MBX-APIKEY": self.api_key}
        response = requests.post(self.base_url + endpoint, params=params, headers=headers)
        return response.json()

    def start_websocket(self, symbol, on_message_callback):
        """Start WebSocket connection for live market data."""
        url = f"{self.ws_url}/{symbol.lower()}@kline_1m"

        def on_message(ws, message):
            """Handle incoming WebSocket messages."""
            data = json.loads(message)
            on_message_callback(data)

        ws = websocket.WebSocketApp(url, on_message=on_message)
        thread = threading.Thread(target=ws.run_forever)
        thread.daemon = True
        thread.start()
        return ws

# Example usage:
# binance = BinanceAPI()
# print(binance.get_account_balance())
