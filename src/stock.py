import mysql.connector
# import sqlite3

class Stock:
    def __init__(self, cursor):
        self.cursor = cursor
        self.table_name = "Stock"

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Stock (
            ID INTEGER AUTO_INCREMENT PRIMARY KEY,
            quantity INTEGER NOT NULL,
            prod_ID INTEGER NOT NULL,
            WH_ID INTEGER NOT NULL,
            minQuantity INTEGER NOT NULL,
            FOREIGN KEY (prod_ID) REFERENCES Product(ID),
            FOREIGN KEY (WH_ID) REFERENCES Warehouse(ID)
        );
        """)

        # Create a row-level trigger to check if stock is below minQuantity after inserting or updating stock.
        self.cursor.execute("""
        DROP TRIGGER IF EXISTS schedule_insert;
        CREATE TRIGGER schedule_insert
        AFTER INSERT ON Stock
        FOR EACH ROW
        BEGIN
            IF NEW.quantity < NEW.minQuantity THEN
                INSERT INTO ToRestock (stock_ID, dateAdded)
                VALUES (NEW.ID, CURDATE());
            END IF;
        END;
        """, multi=True)
        
        # For the update, we must verify that there isn't already a restock order for that stock.
        # ToRestock can have a history of past orders for the same stock, so we must check 
        # if an order already exists by checking if the dateOrdered is NULL on any order with the same stock_ID.
        # If it does, we don't create a new order.
        self.cursor.execute("""
        DROP TRIGGER IF EXISTS schedule_update;
        CREATE TRIGGER schedule_update
        AFTER UPDATE ON Stock
        FOR EACH ROW
        BEGIN
            IF NEW.quantity < NEW.minQuantity AND OLD.quantity >= OLD.minQuantity THEN
                IF NOT EXISTS (
                    SELECT 1
                    FROM ToRestock
                    WHERE stock_ID = NEW.ID AND dateOrdered IS NULL
                ) THEN
                    INSERT INTO ToRestock (stock_ID, dateAdded)
                    VALUES (NEW.ID, CURDATE());
                END IF;
            END IF;
        END;
        """, multi=True)

        # Creates procedure that selects the total quantity of all product group
        procedure_sql = '''
        DROP PROCEDURE IF EXISTS total_quantity;
        CREATE PROCEDURE total_quantity()
	    BEGIN
		    SELECT prod_ID AS ProductID, SUM(quantity) AS totalQuantity 
		    FROM Stock
		    GROUP BY prod_ID;
	    END
        '''

        for _ in self.cursor.execute(procedure_sql, multi=True) :
            pass

    def insert(self, values: list):
        """
        Insert a new stock entry into the Stock table.

        :param values: List of values to insert
        """
        if len(values) == 4:
            self.cursor.execute("""
            INSERT INTO Stock (quantity, prod_ID, WH_ID, minQuantity)
            VALUES (%s, %s, %s, %s);
            """, values)
        else:
            print("Error: inserting to stock expected values (quantity [int], prod_ID [int], WH_ID [int], minQuantity [int])")
