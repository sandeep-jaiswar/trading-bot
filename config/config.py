import os
from dotenv import load_dotenv
import yaml

# Load environment variables from .env file
load_dotenv()

class Config:
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")
    BASE_URL = "https://api.binance.com"
    TESTNET = os.getenv("TESTNET", "false").lower() == "true"

    @staticmethod
    def load_settings():
        """Load settings from a YAML configuration file."""
        with open("config/settings.yaml", "r") as file:
            return yaml.safe_load(file)

# Load settings
settings = Config.load_settings()
