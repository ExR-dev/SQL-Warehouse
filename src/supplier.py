import mysql.connector

class Supplier:
    def __init__(self, cursor):
        self.cursor = cursor
        self.table_name = "Supplier"

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Supplier (
            ID INTEGER AUTO_INCREMENT PRIMARY KEY,
            address TEXT NOT NULL,
            contact TEXT NOT NULL
        );
        """)

    def insert(self, values: list):
        """
        Insert a new supplier into the Supplier table.

        :param values: List of values to insert
        """
        if len(values) == 2:
            self.cursor.execute("""
            INSERT INTO Supplier (address, contact)
            VALUES (%s, %s);
            """, values)
        else:
            print("Error: inserting to supplier expected values (adress [text], contact [text])")
