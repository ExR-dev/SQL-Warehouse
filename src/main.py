import sqlite3


def init_db(conn, cursor):
    """Initialize the database with the required tables."""

    # Create Supplier table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Supplier (
        ID INTEGER PRIMARY KEY,
        address TEXT NOT NULL,
        contact TEXT NOT NULL
    );
    """)

    # Create Product table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Product (
        ID INTEGER PRIMARY KEY,
        sup_ID INTEGER NOT NULL,
        desc TEXT,
        FOREIGN KEY (sup_ID) REFERENCES Supplier(ID)
    );
    """)

    # Create Warehouse table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Warehouse (
        ID INTEGER PRIMARY KEY,
        address TEXT NOT NULL
    );
    """)

    # Create Stock table
    cursor.execute("""
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

    # Create toRestock table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS toRestock (
        ID INTEGER PRIMARY KEY,
        stock_ID INTEGER NOT NULL,
        dateAdded TEXT NOT NULL,
        dateOrdered TEXT,
        FOREIGN KEY (stock_ID) REFERENCES Stock(ID)
    );
    """)

    # Commit connection
    conn.commit()


if __name__ == "__main__":
    # Connect to the SQLite database
    conn = sqlite3.connect('warehouse.db')

    # Create a cursor object
    cursor = conn.cursor()

    # Enable foreign key constraint enforcement
    cursor.execute("PRAGMA foreign_keys = ON;")

    init_db(conn, cursor)

    

    # Close the connection
    conn.close()
