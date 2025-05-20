import mysql.connector
# import sqlite3

class Product:
    def __init__(self, cursor):
        self.cursor = cursor
        self.table_name = "Product"
        self.table_columns = ["ID", "sup_ID", "description"]

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Product (
            ID INTEGER AUTO_INCREMENT PRIMARY KEY,
            sup_ID INTEGER NOT NULL,
            description TEXT,
            FOREIGN KEY (sup_ID) REFERENCES Supplier(ID)
        );
        """)

    def insert(self, values: list):
        """
        Insert a new product into the Product table.

        :param values: List of values to insert
        """
        self.cursor.execute("""
        INSERT INTO Product (sup_ID, description)
        VALUES (%s, %s);
        """, values)
