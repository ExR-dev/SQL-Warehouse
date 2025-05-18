import sqlite3

class Warehouse:
    def __init__(self, cursor: sqlite3.Cursor):
        self.cursor = cursor

        # Create Warehouse table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Warehouse (
            ID INTEGER PRIMARY KEY,
            address TEXT NOT NULL
        );
        """)
