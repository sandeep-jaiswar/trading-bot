import os
from dotenv import load_dotenv
import yaml

# Load environment variables from .env file
load_dotenv()

class Config:
    BINANCE_API_KEY: str = os.getenv("BINANCE_API_KEY")
    BINANCE_SECRET_KEY: str = os.getenv("BINANCE_SECRET_KEY")
    BASE_URL: str = "https://api.binance.com"
    TESTNET: bool = os.getenv("TESTNET", "false").lower() == "true"

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

# Load settings
settings = Config.load_settings()