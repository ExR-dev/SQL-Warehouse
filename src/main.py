import sqlite3
import os

if __name__ == "__main__":
    # Connect to the SQLite database
    conn = sqlite3.connect('warehouse.db')

    # Create a cursor object
    cursor = conn.cursor()

    # Create a table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            sku INTEGER,
            batch_number INTEGER,
            total_cost REAL,
            measurement CHAR(32),
			nr_of INTEGER,
            exp_date DATE,
            PRIMARY KEY (sku, batch_number)
        )
    ''')

    # Ex: Insert a row of data
    cursor.execute('''
        INSERT INTO products (sku, batch_number, total_cost, measurement, nr_of, exp_date)
        VALUES (123456, 1, 19.99, 'kg', 10, '2024-12-31')
    ''')

    # Save (commit) the changes
    conn.commit()

    # Query the database
    cursor.execute('SELECT * FROM products')
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    # Close the connection
    conn.close()
