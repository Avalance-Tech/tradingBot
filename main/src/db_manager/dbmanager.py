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
