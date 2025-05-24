import mysql.connector
from typing import Any

class ToRestock:
    def __init__(self, cursor):
        self.cursor = cursor
        self.table_name = "ToRestock"
        self.table_columns = ["ID", "stock_ID", "dateAdded", "dateOrdered", "orderCount"]

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ToRestock (
            ID INTEGER AUTO_INCREMENT PRIMARY KEY,
            stock_ID INTEGER NOT NULL,
            dateAdded DATETIME NOT NULL,
            dateOrdered DATETIME,
            orderCount INTEGER DEFAULT NULL,
            FOREIGN KEY (stock_ID) REFERENCES Stock(ID)
        );
        """)

        upgrade_database_add_orderCount_sql ="""
        DROP PROCEDURE IF EXISTS upgrade_database_add_orderCount;
        CREATE PROCEDURE upgrade_database_add_orderCount()
        BEGIN
            -- add a column safely
            IF NOT EXISTS( (SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=DATABASE()
                    AND COLUMN_NAME='orderCount' AND TABLE_NAME='ToRestock') ) THEN
                ALTER TABLE ToRestock 
                ADD orderCount INTEGER DEFAULT NULL
                AFTER dateOrdered;
            END IF;
        END;
        CALL upgrade_database_add_orderCount();
        """

        for _ in self.cursor.execute(upgrade_database_add_orderCount_sql, multi=True):
            pass


        # Create a procedure to view all restock associated to a specific warehouse
        warehouse_torestock_list_sql = '''
        DROP PROCEDURE IF EXISTS warehouse_torestock_list;
        CREATE PROCEDURE warehouse_torestock_list(IN active_warehouse_ID INT)
        BEGIN
            SELECT r.ID AS restockID, r.stock_ID AS ProductID, r.dateAdded AS DateAdded
            FROM ToRestock r
            INNER JOIN Stock s ON r.stock_ID = s.ID
            WHERE s.WH_ID = active_warehouse_ID;
        END
        '''

        for _ in self.cursor.execute(warehouse_torestock_list_sql, multi=True):
            pass

        # Get all active restock orders, ordered by dateAdded
        get_order_list_sql = '''
        DROP PROCEDURE IF EXISTS get_order_list;
        CREATE PROCEDURE get_order_list(IN warehouse_id INT)
        BEGIN
            SELECT Stock.ID AS stock_ID, Product.description AS product_desc, 
                   Supplier.address AS supplier_name, Supplier.contact AS supplier_contact, 
                   Stock.quantity AS curr_stock_count, Stock.minQuantity - Stock.quantity AS min_order_count, 
                   ToRestock.dateAdded AS date_added
            FROM ToRestock
            JOIN Stock ON ToRestock.stock_ID = Stock.ID
            JOIN Product ON Stock.prod_ID = Product.ID
            JOIN Supplier ON Product.sup_ID = Supplier.ID
            WHERE Stock.WH_ID = warehouse_id AND ToRestock.dateOrdered IS NULL
            ORDER BY ToRestock.dateAdded ASC;
        END
        '''

        for _ in self.cursor.execute(get_order_list_sql, multi=True):
            pass
    
    def insert(self, values: list[str]):
        """
        Insert a new order into the ToRestock table.

        :param values: List of values to insert
        """
        if len(values) == 1:
            self.cursor.execute("""
            INSERT INTO ToRestock (stock_ID, dateAdded)
            VALUES (%s, NOW());
            """, values)
        else:
            print("Error: inserting to ToRestock expected values (stock_ID [int])")

    def get_order_list(self, warehouse_id: int) -> list[Any]:
        """
        Get a list of all active orders, sorted from oldest to newest.
        """
        self.cursor.execute("""
        SELECT ToRestock.ID, ToRestock.dateAdded, ToRestock.dateOrdered, Stock.quantity, Product.description
        FROM ToRestock
        JOIN Stock ON ToRestock.stock_ID = Stock.ID
        JOIN Product ON Stock.prod_ID = Product.ID
        WHERE Stock.WH_ID = %s
        ORDER BY ToRestock.dateAdded ASC;
        """, (warehouse_id,))

        return self.cursor.fetchall()
