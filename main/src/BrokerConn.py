import alpaca_trade_api

API_KEY = "PK0DPZ9ECWPW8L8XDQ30"
SECRET_API_KEY = "B0GoMsQVFvkFb9Lg5vTmGuhCOO0TQhO4MYOPee1m"
BASE_URL = "https://paper-api.alpaca.markets"

# Initialize the Alpaca API client
api = alpaca_trade_api.REST(API_KEY, SECRET_API_KEY, BASE_URL, api_version='v2')

def make_trade(Stock: str, Amount: float) -> dict:
    1

def leave_trade(Stock: str, Amount: float) -> dict:
    1

def get_info(Stock: str) -> dict:
    1

def get_balance() -> float:
    return api.get_account().cash

print(get_balance())
