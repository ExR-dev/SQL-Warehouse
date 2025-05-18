import sqlite3

def get_order_list(cursor, warehouse_id):
    """
    Get a list of all active orders, sorted from oldest to newest.
    """
    cursor.execute("""
    SELECT ToRestock.ID, ToRestock.dateAdded, ToRestock.dateOrdered, Stock.quantity, Product.description
    FROM ToRestock
    JOIN Stock ON ToRestock.stock_ID = Stock.ID
    JOIN Product ON Stock.prod_ID = Product.ID
    WHERE Stock.WH_ID = ?
    ORDER BY ToRestock.dateAdded ASC;
    """, (warehouse_id,))
    
    return cursor.fetchall()