import mysql.connector

class Stock:

    def __init__(self, cursor):
        def execute_multi_sql(self, procedure_sql : str):
            for _ in self.cursor.execute(procedure_sql, multi=True):
                pass

        self.cursor = cursor
        self.table_name = "Stock"
        self.table_columns = ["ID", "quantity", "prod_ID", "WH_ID", "minQuantity"]

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Stock (
            ID INTEGER AUTO_INCREMENT PRIMARY KEY,
            quantity INTEGER NOT NULL,
            prod_ID INTEGER NOT NULL,
            WH_ID INTEGER NOT NULL,
            minQuantity INTEGER NOT NULL,
            FOREIGN KEY (prod_ID) REFERENCES Product(ID),
            FOREIGN KEY (WH_ID) REFERENCES Warehouse(ID),
            UNIQUE KEY prod_wh_key (prod_ID, WH_ID)
        );
        """)

        # Create a row-level trigger to check if stock is below minQuantity after inserting or updating stock.
        schedule_insert_sql = """
        DROP TRIGGER IF EXISTS schedule_insert;
        CREATE TRIGGER schedule_insert
        AFTER INSERT ON Stock
        FOR EACH ROW
        BEGIN
            IF NEW.quantity < NEW.minQuantity THEN
                INSERT INTO ToRestock (stock_ID, dateAdded)
                VALUES (NEW.ID, NOW());
            END IF;
        END;
        """

        for _ in self.cursor.execute(schedule_insert_sql, multi=True):
            pass
        
        # For the update, we must verify that there isn't already a restock order for that stock.
        # ToRestock can have a history of past orders for the same stock, so we must check 
        # if an order already exists by checking if the dateOrdered is NULL on any order with the same stock_ID.
        # If it does, we don't create a new order.
        schedule_update_sql = """
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
                    VALUES (NEW.ID, NOW());
                END IF;
            END IF;
        END;
        """

        execute_multi_sql(self, schedule_update_sql)

        # Create a trigger to update the ToRestock table when stock is updated
        # Looks through the toRestock table to see if an active restock order exists for the stock.
        # If it does, it updates the dateOrdered to the current date and the orderCount to the change in quantity.
        # If it doesn't, it adds a new restock order and completes it immediately.
        complete_schedule_sql = """
        DROP TRIGGER IF EXISTS complete_schedule;
        CREATE TRIGGER complete_schedule
        AFTER UPDATE ON Stock
        FOR EACH ROW
        BEGIN
            IF NEW.quantity > OLD.quantity OR (NEW.quantity >= NEW.minQuantity AND OLD.quantity < OLD.minQuantity) THEN
                -- Check if there is an existing order for this stock that has not been ordered yet
                IF EXISTS (
                    SELECT 1
                    FROM ToRestock
                    WHERE stock_ID = NEW.ID AND dateOrdered IS NULL
                ) THEN
                    -- Update the existing order with the new quantity difference
                    UPDATE ToRestock
                    SET dateOrdered = NOW(), orderCount = (NEW.quantity - OLD.quantity)
                    WHERE stock_ID = NEW.ID AND dateOrdered IS NULL;
                ELSEIF NEW.quantity > OLD.quantity THEN
                    -- Create a new order for this stock
                    INSERT INTO ToRestock (stock_ID, dateAdded, dateOrdered, orderCount)
                    VALUES (NEW.ID, NOW(), NOW(), (NEW.quantity - OLD.quantity));
                END IF;
            END IF;
        END;
        """

        execute_multi_sql(self, complete_schedule_sql)

        # Creates procedure that selects the total quantity of all product group
        total_quantity_sql = '''
        DROP PROCEDURE IF EXISTS total_quantity;
        CREATE PROCEDURE total_quantity()
	    BEGIN
		    SELECT p.ID AS ProductID, p.description AS Description, SUM(s.quantity) AS totalQuantity 
		    FROM Stock s 
            RIGHT JOIN product p ON s.prod_id = p.ID 
		    GROUP BY p.ID
            ORDER BY p.ID ASC;
	    END
        '''

        execute_multi_sql(self, total_quantity_sql)
        
        # Creates a procedure to view all stocks belonging to a specific warehouse
        warehouse_inventory_sql = """
        DROP PROCEDURE IF EXISTS warehouse_inventory;
        CREATE PROCEDURE warehouse_inventory(IN active_warehouse_ID INT)
        BEGIN
            SELECT s.ID AS StockID, s.prod_ID AS ProductID, s.quantity AS Quantity, s.minQuantity AS MinQuantity, p.description AS Description
            FROM Stock s
            LEFT JOIN product p ON s.prod_ID  = p.ID
            WHERE active_warehouse_ID = s.WH_ID;
        END
        """

        execute_multi_sql(self, warehouse_inventory_sql)

        # Create a procedure to update a stocks quantity relative to its current,
        # using  stock_id, and quantity change
        update_stock_quantity_sql ='''
        DROP PROCEDURE IF EXISTS update_stock_quantity;
        CREATE PROCEDURE update_stock_quantity(IN stockID INTEGER, IN quantChange INTEGER)
        BEGIN
            UPDATE stock
                SET quantity = quantity + quantChange
                WHERE ID = stockID;
        END
        '''

        execute_multi_sql(self, update_stock_quantity_sql)

        # Create a procedure to set a stocks quantity
        set_stock_quantity_sql = '''
        DROP PROCEDURE IF EXISTS set_stock_quantity;
        CREATE PROCEDURE set_stock_quantity(IN stockID INTEGER, IN newQuantity INTEGER)
        BEGIN
            UPDATE stock
                SET quantity = newQuantity
                WHERE ID = stockID;
        END
        '''
        execute_multi_sql(self, set_stock_quantity_sql)

        update_stock_minQuantity_sql = '''
        DROP PROCEDURE IF EXISTS update_stock_minQuantity;
        CREATE PROCEDURE update_stock_minQuantity(IN stockID INTEGER, IN minQuantityChange INTEGER)
        BEGIN
            UPDATE Stock
                SET minQuantity = minQuantity + minQuantityChange
                WHERE ID = stockID;
        END
        '''

        execute_multi_sql(self, update_stock_minQuantity_sql)

        set_stock_minQuantity_sql = '''
        DROP PROCEDURE IF EXISTS set_stock_minQuantity;
        CREATE PROCEDURE set_stock_minQuantity(IN stockID INTEGER, IN newMinQuantity INTEGER)
        BEGIN
            UPDATE stock
                SET minQuantity = newMinQuantity
                WHERE ID = stockID;
        END
        '''

        execute_multi_sql(self, set_stock_minQuantity_sql)

    def insert(self, values: list[str]):
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

