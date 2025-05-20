import mysql.connector

class Supplier:
    def __init__(self, cursor):
        self.cursor = cursor
        self.table_name = "Supplier"

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Supplier (
            ID INTEGER PRIMARY KEY,
            address TEXT NOT NULL,
            contact TEXT NOT NULL
        );
        """)

    def insert(self, values: list):
        """
        Insert a new supplier into the Supplier table.

        :param values: List of values to insert
        """
        self.cursor.execute("""
        INSERT INTO Supplier (address, contact)
        VALUES (?, ?);
        """, values)
        
