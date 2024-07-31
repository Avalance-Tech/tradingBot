import os
import alpaca_trade_api
import time
from Exceptions import InsuffecientFunds
from datetime import datetime, timedelta
from dotenv import load_dotenv
from alpaca_trade_api.rest import APIError
load_dotenv()

API_KEY = "PK0DPZ9ECWPW8L8XDQ30"
SECRET_API_KEY = os.getenv("SECRET_ALPACA_KEY")
BASE_URL = "https://paper-api.alpaca.markets"

class BrokerConn:
    def __init__(self, API_KEY, SECRET_KEY, BASE_URL = "https://paper-api.alpaca.markets"):
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.BASE_URL = BASE_URL
        # Initialize the Alpaca API client
        self.api = alpaca_trade_api.REST(API_KEY, SECRET_KEY, BASE_URL, api_version="v2")

    def create_trade(self, Stock: str, Amount: float) -> dict:
        estimatedCost = self.api.get_latest_trade(Stock).price * Amount
        if estimatedCost > self.get_balance():
            raise InsuffecientFunds(self.get_balance(), estimatedCost)

        order = self.api.submit_order(
            symbol = Stock,
            qty = Amount,
            side="buy",
            type="market",
            time_in_force="ioc"  # immediate or cancelled
        )
        
        while True:
            filledOrder = self.api.get_order(order.id)
            if filledOrder.status == "filled":
                break
            elif filledOrder.status == "canceled":
                print("Order cancelled because market is likely closed or couldnt trade the stocks immediately")
                return
            time.sleep(1)  # Wait for a second before checking again
        
        tradeData = {
            "Amount": Amount,
            "Price": float(filledOrder.filled_avg_price),
            "Time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")  # current UTC time
        }

        return tradeData
    

    def leave_trade(self, Stock: str, Amount: float) -> dict:
        # Check if the stock is in the portfolio
        try:
            position = self.api.get_position(Stock)
        except APIError:
            raise ValueError("Stock not in portfolio")
        # If the amount to sell is more than available, raise ValueError
        if int(position.qty) < Amount:
            raise ValueError(f"Not enough shares of {Stock} to sell. Available: {position.qty}, Requested: {Amount}")
        
        # Place a market order to sell the stock
        order = self.api.submit_order(
            symbol = Stock,
            qty = Amount,
            side = "sell",
            type = "market",
            time_in_force = "ioc"
        )
        
        # Wait for the order to be filled
        while True:
            newOrder = self.api.get_order(order.id)
            if newOrder.status == "filled":
                break
            elif newOrder.status == "canceled":
                print("couldnt sell because market is likely closed")
                return
            time.sleep(1) # Wait for a second before checking again
        
        # Fetch the trade data
        tradeData = {
            "Cash": float(newOrder.filled_avg_price) * Amount,
            "Price": float(newOrder.filled_avg_price),
            "Time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")  # Use the current UTC time
        }

        return tradeData


    def get_info(self, Stock: str, time = None) -> dict:
        # Default time to current time if not provided
        if time is None:
            time = datetime.utcnow()
        else:
            time = datetime.fromisoformat(time.replace("Z", "+00:00"))

        # Format time to string RFC3391 format
        startTime = (time - timedelta(minutes = 1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        endTime = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Fetch bar data for the stock symbol
        barset = self.api.get_bars(Stock, "1min", startTime, endTime)
        print(barset)
        # Check if symbol exists in the response
        if not barset:
            raise ValueError(f"No data available for stock symbol '{Stock}'")
        
        # Get the most recent bar data
        bar = barset[0]
        
        # Return stock information
        return {
            "Price": bar.c,          # Close price of the stock
            "Volume": bar.v,         # Volume of trades
            "Time": bar.t.strftime("%Y-%m-%dT%H:%M:%SZ") # Time of the bar data
        }

    def get_balance(self) -> float:
        return float(self.api.get_account().cash)

trader = BrokerConn(API_KEY, SECRET_API_KEY)
print(trader.leave_trade("NVDA", 2))

