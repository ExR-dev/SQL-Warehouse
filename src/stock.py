import sqlite3

class Stock:
    def __init__(self, cursor: sqlite3.Cursor):
        self.cursor = cursor

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Stock (
            ID INTEGER PRIMARY KEY,
            quantity INTEGER NOT NULL,
            prod_ID INTEGER NOT NULL,
            WH_ID INTEGER NOT NULL,
            minQuantity INTEGER NOT NULL,
            FOREIGN KEY (prod_ID) REFERENCES Product(ID),
            FOREIGN KEY (WH_ID) REFERENCES Warehouse(ID)
        );
        """)

        # Add low-level trigger to check if stock is below minQuantity after inserting or updating stock
        # and add a restock order if it is
        self.cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS schedule
        AFTER INSERT ON Stock
        FOR EACH ROW
        BEGIN
            INSERT INTO ToRestock (stock_ID, dateAdded)
            VALUES (NEW.ID, DATE('now'));
        END;
        """)
