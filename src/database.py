import sqlite3
import warehouse
import supplier
import product
import stock
import toRestock


class Database:
    def __init__(self, db_name: str):
        """
        Initialize the database connection and create tables if they don't exist.

        :param db_name: Name of the database file
        """

        self.db_file = db_name
        if db_name.find(".") == -1:
            self.db_file += ".db"

        # Open or create database file
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        
        # Enable foreign key constraint enforcement
        self.cursor.execute("PRAGMA foreign_keys = ON;")

        self.warehouse = warehouse.Warehouse(self.cursor)
        self.supplier = supplier.Supplier(self.cursor)
        self.product = product.Product(self.cursor)
        self.stock = stock.Stock(self.cursor)
        self.toRestock = toRestock.ToRestock(self.cursor)

        # Commit connection
        self.conn.commit()
        self.open = True

    def close(self):
        self.conn.close()
        self.open = False

    def is_open(self) -> bool:
        return self.open
