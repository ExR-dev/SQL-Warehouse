import sqlite3
import os


if __name__ == "__main__":
    # Connect to the SQLite database
    conn = sqlite3.connect('example.db')

    # Create a cursor object
    cursor = conn.cursor()

    # Create a table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            sku INTEGER PRIMARY KEY,
            batch_number INTEGER PRIMARY KEY,
            total_cost REAL,
            measurement TEXT,
			nr_of INTEGER,
            exp_date DATE
        )
    ''')


    # Ex:
    # Insert a row of data
    cursor.execute('''
        INSERT INTO users (name, age)
        VALUES ('Alice', 30)
    ''')

    # Save (commit) the changes
    conn.commit()

    # Query the database
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    # Close the connection
    conn.close()
