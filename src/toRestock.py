import mysql.connector
# import sqlite3
from typing import Any

class ToRestock:
    def __init__(self, cursor):
        self.cursor = cursor
        self.table_name = "ToRestock"
        self.table_columns = ["ID", "stock_ID", "dateAdded", "dateOrdered"]

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ToRestock (
            ID INTEGER AUTO_INCREMENT PRIMARY KEY,
            stock_ID INTEGER NOT NULL,
            dateAdded TEXT NOT NULL,
            dateOrdered TEXT,
            FOREIGN KEY (stock_ID) REFERENCES Stock(ID)
        );
        """)
    
    def insert(self, values: list):
        """
        Insert a new order into the ToRestock table.

        :param values: List of values to insert
        """
        if len(values) == 1:
            self.cursor.execute("""
            INSERT INTO ToRestock (stock_ID, dateAdded)
            VALUES (%s, CURDATE());
            """, values)
        else:
            print("Error: inserting to ToRestock expected values (stock_ID [int])")

    def get_order_list(self, warehouse_id: int) -> list[Any]:
        """
        Get a list of all active orders, sorted from oldest to newest.
        """
        self.cursor.execute("""
        SELECT ToRestock.ID, ToRestock.dateAdded, ToRestock.dateOrdered, Stock.quantity, Product.description
        FROM ToRestock
        JOIN Stock ON ToRestock.stock_ID = Stock.ID
        JOIN Product ON Stock.prod_ID = Product.ID
        WHERE Stock.WH_ID = ?
        ORDER BY ToRestock.dateAdded ASC;
        """, (warehouse_id,))

        return self.cursor.fetchall()
