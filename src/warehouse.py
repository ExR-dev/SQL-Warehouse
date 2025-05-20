import sqlite3

class Warehouse:
    def __init__(self, cursor: sqlite3.Cursor):
        self.cursor = cursor
        self.table_name = "Warehouse"

        # Create Warehouse table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Warehouse (
            ID INTEGER PRIMARY KEY,
            address TEXT NOT NULL
        );
        """)

    def insert(self, values: list):
        """
        Insert a new warehouse into the Warehouse table.

        :param values: List of values to insert
        """
        self.cursor.execute("""
        INSERT INTO Warehouse (address)
        VALUES (?);
        """, values)
