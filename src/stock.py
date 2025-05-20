import sqlite3

class Stock:
    def __init__(self, cursor: sqlite3.Cursor):
        self.cursor = cursor
        self.table_name = "Stock"

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

        # Create a row-level trigger to check if stock is below minQuantity after inserting or updating stock.
        self.cursor.execute(f"""
        CREATE TRIGGER IF NOT EXISTS schedule_insert
        AFTER INSERT ON Stock
        FOR EACH ROW
        WHEN NEW.quantity < NEW.minQuantity
        BEGIN
            INSERT INTO ToRestock (stock_ID, dateAdded)
            VALUES (NEW.ID, DATE('now'));
        END;
        """)
        
        # For the update, we must verify that there isn't already a restock order for that stock.
        # ToRestock can have a history of past orders for the same stock, so we must check 
        # if an order already exists by checking if the dateOrdered is NULL on any order with the same stock_ID.
        # If it does, we don't create a new order.
        self.cursor.execute(f"""
        CREATE TRIGGER IF NOT EXISTS schedule_update
        AFTER UPDATE ON Stock
        FOR EACH ROW
        WHEN NEW.quantity < NEW.minQuantity AND OLD.quantity >= OLD.minQuantity
        BEGIN
            INSERT INTO ToRestock (stock_ID, dateAdded)
            SELECT NEW.ID, DATE('now')
            WHERE NOT EXISTS (
                SELECT 1
                FROM ToRestock
                WHERE stock_ID = NEW.ID AND dateOrdered IS NULL
            );
        END;
        """)


    def insert(self, values: list):
        """
        Insert a new stock entry into the Stock table.

        :param values: List of values to insert
        """
        self.cursor.execute("""
        INSERT INTO Stock (quantity, prod_ID, WH_ID, minQuantity)
        VALUES (?, ?, ?, ?);
        """, values)
