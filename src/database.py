import mysql.connector
from mysql.connector import Error
from typing import Optional
import tableUtils
import warehouse
import supplier
import product
import stock
import toRestock


class Database:
    def init(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                port=3306,
                user='root',
                password='0000'
            )

            if self.conn.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print("Error while connecting to MySQL", e)
            return
        finally:
            if 'connection' in locals() and self.conn.is_connected():
                self.conn.close()
                print("MySQL connection is closed")

        self.open = True
        self.cursor = self.conn.cursor()

        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name};")
        self.cursor.execute(f"USE {self.db_name};")
        
        self.warehouse = warehouse.Warehouse(self.cursor)
        self.supplier = supplier.Supplier(self.cursor)
        self.product = product.Product(self.cursor)
        self.stock = stock.Stock(self.cursor)
        self.toRestock = toRestock.ToRestock(self.cursor)

    def close(self):
        if self.open:
            self.conn.close()
            self.open = False


    def __init__(self, db_name: str):
        """
        Initialize the database connection and create tables if they don't exist.

        :param db_name: Name of the database file
        """
        self.db_name = db_name
        self.init()

    def __del__(self):
        """
        Close the database connection when the object is deleted.
        """
        if self.open:
            self.close()


    def print_table(self, table: str, columns: Optional[list[str]] = None):
        """
        Print the contents of a specified table.

        :param table: Name of the table to print
        :param columns: List of columns to print (optional)
        """
        select_origin = "*"
        if isinstance(columns, (list, tuple)):
            select_origin = ', '.join(columns)

        table = table.lower()
        table_class = None
        if table == "warehouse":
            table_class = self.warehouse
        elif table == "supplier":
            table_class = self.supplier
        elif table == "product":
            table_class = self.product
        elif table == "stock":
            table_class = self.stock
        elif table == "torestock":
            table_class = self.toRestock
        else:
            raise ValueError(f"Unknown table: {table}")

        self.cursor.execute(f"SELECT {select_origin} FROM {table_class.table_name};")
        rows = self.cursor.fetchall()

        # Determine the max character length of all columns
        column_names = (table_class.table_columns) if (select_origin == "*") else (select_origin)
        tableUtils.print_table(column_names, rows)

    def insert(self, table: str, values: list[str]):
        """
        Insert values into a specified table.

        :param table: Name of the table to insert into
        :param values: List of values to insert
        """
        table = table.lower()
        if table == "warehouse":
            self.warehouse.insert(values)
        elif table == "supplier":
            self.supplier.insert(values)
        elif table == "product":
            self.product.insert(values)
        elif table == "stock":
            self.stock.insert(values)
        elif table == "torestock":
            self.toRestock.insert(values)
        else:
            raise ValueError(f"Unknown table: {table}")

    def update(self, table: str, set_values: list[str], where: str):
        """
        Update values in a specified table.

        :param table: Name of the table to update
        :param set_values: List of values to set
        :param where: WHERE clause for the update
        """
        set_str = ', '.join([f"{col}" for col in set_values])
        set_str = set_str.replace('=', ' = ')

        str_cmd = f"""
        UPDATE {table}
        SET {set_str}
        WHERE {where};
        """
        print(str_cmd)

        self.cursor.execute(str_cmd)

    def commit(self):
        """
        Commit the current transaction.
        """
        self.conn.commit()

    def is_open(self) -> bool:
        return self.open
