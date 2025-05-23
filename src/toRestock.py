import mysql.connector
from typing import Any

class ToRestock:
    def __init__(self, cursor):
        self.cursor = cursor
        self.table_name = "ToRestock"
        self.table_columns = ["ID", "stock_ID", "dateAdded", "dateOrdered"]

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ToRestock (
            ID INTEGER AUTO_INCREMENT PRIMARY KEY,
            stock_ID INTEGER NOT NULL,
            dateAdded TEXT NOT NULL,
            dateOrdered TEXT,
            FOREIGN KEY (stock_ID) REFERENCES Stock(ID)
        );
        """)

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
    
    def insert(self, values: list[str]):
        """
        Insert a new order into the ToRestock table.

        :param values: List of values to insert
        """
        if len(values) == 1:
            self.cursor.execute("""
            INSERT INTO ToRestock (stock_ID, dateAdded)
            VALUES (%s, CURDATE());
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
        WHERE Stock.WH_ID = ?
        ORDER BY ToRestock.dateAdded ASC;
        """, (warehouse_id,))

        return self.cursor.fetchall()
