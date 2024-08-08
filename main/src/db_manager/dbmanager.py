"""the file that contains the dbmanager class"""
import json
from Exceptions import InsuffecientFunds

InsuffecientFunds()


class DbManager:
    """the class that manages the database"""

    def __init__(self, db_path: str) -> None:
        """initializes the dbmanager class

        Args:
            db_path (str): path to the data json file
        """
        self.db_path = db_path

    def store_data(self, data: dict) -> None:
        """initializes the database

        Args:
            data (dict): the data to initialize the database with
        """
        with open(self.db_path, "w") as file:
            json.dump(data, file)

    def store_trade(self, trade: dict) -> None:
        """stores a trade in the database

        Args:
            trade (dict): the trade to store
        """
        with open(self.db_path, "r") as file:
            data = json.load(file)

        data["trades"].append(trade)

        with open(self.db_path, "w") as file:
            json.dump(data, file)

    def get_trades(self, user_id: int) -> list:
        """gets the trades of a user

        Args:
            user_id (int): the id of the user

        Returns:
            list: the trades of the user
        """
        with open(self.db_path, "r") as file:
            data = json.load(file)

        trades = []
        for trade in data["trades"]:
            if trade["user_id"] == user_id:
                trades.append(trade)

        return trades

    def store_sl(self, stock: str, price: float, percentage: int) -> None:
        """stores a stop loss in the database

        Args:
            stock (str): the stock to set the stop loss for
            price (float): the price to set the stop loss at
            percentage (int): the percentage to set the stop loss at
        """
        with open(self.db_path, "r") as file:
            data = json.load(file)

        data["stop_losses"].append(
            {"stock": stock, "price": price, "percentage": percentage})

        with open(self.db_path, "w") as file:
            json.dump(data, file)

    def remove_sl(self, stock: str, price: float, percentage: int) -> None:
        """removes a stop loss from the database

        Args:
            stock (str): the stock to remove the stop loss from
            price (float): the price to remove the stop loss at
            percentage (int): the percentage to remove the stop loss at
        """
        with open(self.db_path, "r") as file:
            data = json.load(file)

        for sl in data["stop_losses"]:
            if sl["stock"] == stock and sl["price"] == price and sl["percentage"] == percentage:
                data["stop_losses"].remove(sl)

        with open(self.db_path, "w") as file:
            json.dump(data, file)

    def get_sl(self, stock: str) -> dict:
        """gets the stop loss for a stock
        Args:
            stock (str): the stock to get the stop loss for

        Returns:
            dict: the stop loss for the stock
        """
        with open(self.db_path, "r") as file:
            data = json.load(file)

        for sl in data["stop_losses"]:
            if sl["trades"] == stock:
                return sl
