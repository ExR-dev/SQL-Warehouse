import sqlite3

class Product:
    def __init__(self, cursor: sqlite3.Cursor):
        self.cursor = cursor

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Product (
            ID INTEGER PRIMARY KEY,
            sup_ID INTEGER NOT NULL,
            description TEXT,
            FOREIGN KEY (sup_ID) REFERENCES Supplier(ID)
        );
        """)
