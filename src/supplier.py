import sqlite3

class Supplier:
    def __init__(self, cursor: sqlite3.Cursor):
        self.cursor = cursor

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Supplier (
            ID INTEGER PRIMARY KEY,
            address TEXT NOT NULL,
            contact TEXT NOT NULL
        );
        """)
        
