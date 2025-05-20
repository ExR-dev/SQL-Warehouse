import sqlite3
from typing import Optional
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
        self.commit()
        self.open = True

    def __del__(self):
        """
        Close the database connection when the object is deleted.
        """
        if self.open:
            self.close()


    def print_table(self, table: str, columns: Optional[list] = None):
        """
        Print the contents of a specified table.

        :param table: Name of the table to print
        :param columns: List of columns to print (optional)
        """
        select_origin = "*"
        if isinstance(columns, (list, tuple)):
            select_origin = ', '.join(columns)

        self.cursor.execute(f"SELECT {select_origin} FROM {table};")
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)

    def insert(self, table: str, values: list):
        """
        Insert values into a specified table.

        :param table: Name of the table to insert into
        :param values: List of values to insert
        """
        if table == "warehouse":
            self.warehouse.insert(values)
        elif table == "supplier":
            self.supplier.insert(values)
        elif table == "product":
            self.product.insert(values)
        elif table == "stock":
            self.stock.insert(values)
        elif table == "toRestock":
            self.toRestock.insert(values)
        else:
            print(f"Unknown table: {table}")
            

    def commit(self):
        """
        Commit the current transaction.
        """
        self.conn.commit()

    def close(self):
        self.conn.close()
        self.open = False

    def is_open(self) -> bool:
        return self.open
