import mysql.connector
# import sqlite3

class Warehouse:
    def __init__(self, cursor):
        self.cursor = cursor
        self.table_name = "Warehouse"
        self.table_columns = ["ID", "address"]

        # Create Warehouse table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Warehouse (
            ID INTEGER AUTO_INCREMENT PRIMARY KEY,
            address TEXT NOT NULL
        );
        """)

    def insert(self, values: list[str]):
        """
        Insert a new warehouse into the Warehouse table.

        :param values: List of values to insert
        """
        if len(values) == 1:
            self.cursor.execute("""
            INSERT INTO Warehouse (address)
            VALUES (%s);
            """, values)
        else:
            print("Error: inserting to warehouse expected values (address [text])")
