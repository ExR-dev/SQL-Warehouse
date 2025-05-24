import mysql.connector
from database import Database
import tableUtils
from mysql.connector.cursor import MySQLCursor
from mysql.connector import Error
from enum import Enum

class Main_Choices(Enum):
    exit = "0"
    Select_Warehouse = "1"
    Update_Database = "2"
    devmode = "dev"

class Warehouse_Menu_Choices(Enum):
    Back = "0"
    View = "1"
    Update = "2"

class Warehouse_View_Menu_Choices(Enum):
    Back = "0"
    Inventory = "1"
    Retock_Needed = "2"

class Warehouse_Update_Menu_Choices(Enum):
    Back = "0"
    Update_Stock = "1"
    New_Stock = "2"
    Change_Adress = "3"
    
class Warehouse_Stock_Menu_Choices(Enum):
    Back = "0"
    Add_or_Sub_Quantity = "1"
    Set_Quantity = "2"
    Add_or_Sub_Minimum_Quantity = "3"
    Set_Minimum_Quantity = "4"

def print_menu_options(menu_class : Enum):
    for option in menu_class:
        print(f"{option.value}. {option.name.capitalize()}")

def main_menu(db : Database) -> bool:
    menu_open = True
    devmode = False
    cursor = db.cursor
    curr_warehouse = None


    while menu_open:
        print("\n==== Warehouse Inventory Main Menu ====")
        print(f"Current warehouse: {curr_warehouse}")
        print_menu_options(Main_Choices)

        try:
            choice = input("Choose an option:> ")
        except:
            print("\nError: Closing Menu")
            menu_open = False

        if choice == Main_Choices.exit.value:
            print("Closing Menu")
            menu_open = False

        elif choice == Main_Choices.devmode.value:
            print("Entering development mode")
            menu_open = False
            devmode = True

        elif choice == Main_Choices.Select_Warehouse.value:
            curr_warehouse = warehouse_selection(cursor, curr_warehouse)
            warehouse_menu(cursor, curr_warehouse)
            menu_open = True

    return devmode

def warehouse_selection(cursor : MySQLCursor, curr_warehouse : int | None) -> str:
    # Query the warehouse table print out as an option list move to next step in menu
    section_open = True
    options = []

    print("======== Select a Warehouse =========")
    print("q to abort selection")
    print("[Warehouse ID, Adresss]")
    cursor.execute("SELECT * FROM warehouse;")

    while section_open:
        for result in cursor:
            print(result)
            # Adds warehouse ID as a string to option list
            options.append(str(result[0]))

        try:
            choice = input("> ")
        except:
            print("\nError closing section no warehouse will be selected")
            choice = None
            return choice

        if choice == "q":
            try:
                confirm = input("Aborting warehouse selection do you wish to keep currently selected warehouse? (y/n)\n> ").lower()
            except:
                print("\nError closing section no warehouse will be selected")
                choice = None
                return choice
            
            if confirm == "y":
                choice = curr_warehouse
                section_open = False
            
            else:
                choice = None
                section_open = False 

        elif choice in options:
            section_open = False

        else:
            print("Not a known warehouse please try again")


    return choice

def stock_selection(cursor : MySQLCursor, curr_warehouse : int | None):
    section_open = True
    options =[]
    print("======== Select a Stock =========")
    print("q to abort selection")
    print("[Stock ID, Quantity, Description]")
    if curr_warehouse is None:
        cursor.execute("SELECT * FROM Stock;")
        results = [cursor.fetchall()] # Match stored_results() style

    else:
        results = cursor.execute(f"CALL warehouse_inventory({curr_warehouse});",multi=True)

    while section_open:
        for result_set in results:
            for row in result_set:
                print(row)
                # Adds Stock ID as a string to option list
                options.append(str(row[0]))

        try:
            choice = input("> ")
        except:
            print("\nError closing section no warehouse will be selected")
            choice = None
            return choice
        
        if choice == "q":
            print("Aborting selection")
            choice = None
            section_open = False

        elif choice in options:
            print(f"Selecting stock: {choice}")
            section_open = False
        
        else:
            print("Unkown stock ID, try again")

    return choice

def warehouse_view_menu(cursor : MySQLCursor, curr_warehouse : int):
    section_open = True

    while section_open:
        print("==== Warehouse View Menu ====")
        print(f"Current warehouse: {curr_warehouse}")
        print_menu_options(Warehouse_View_Menu_Choices)

        try:
            choice = input("Choose an option:> ")
        except:
            print("\nError: Closing Menu")
            section_open = False
    
        if choice == Warehouse_View_Menu_Choices.Back.value:
            print("Backing out")
            section_open = False
        
        elif choice == Warehouse_View_Menu_Choices.Inventory.value:
            sql_inventory_view = f'''CALL warehouse_inventory({curr_warehouse});'''
            empty = True
            print("==== Warehouse Inventory ====")
            print("[Product ID, Quantity, Description]")

            try:    
                for result in cursor.execute(sql_inventory_view, multi=True):
                    if result.with_rows:
                        empty = False
                        rows = cursor.fetchall()
                        for row in rows:
                            empty = False
                            print(row)
                if empty:
                    print("Empty")

            except Exception as e:
                print("Error: Please Conntact system admin")
                print(f"SQL Error: {e}")
                
            done = False
            while not done:
                try:
                    confirm = input("Continue? (y/n): ")
                except:
                    print("\nError: Closing Menu")
                    section_open = False
                
                if confirm == "y":
                    done = True

        elif choice == Warehouse_View_Menu_Choices.Retock_Needed.value:
            sql_torestock_needed =f'''CALL warehouse_torestock_list({curr_warehouse});'''
            empty = True
            print("==== Warehouse Restock List ====")
            print("[Restock ID, Product ID, Date Added]")

            try:    
                for result in cursor.execute(sql_torestock_needed, multi=True):
                    if result.with_rows:
                        field_names = [i[0] for i in result.description]
                        rows = cursor.fetchall()
                        tableUtils.print_table(field_names, rows)
                if empty:
                    print("Empty")

            except Exception as e:
                print("Error: Please Conntact system admin")
                print(f"SQL Error: {e}")

            done = False
            while not done:
                try:
                    confirm = input("Continue? (y/n): ")
                except:
                    print("\nError: Closing Menu")
                    section_open = False
                
                if confirm == "y":
                    done = True

# Not Done Currently working on
def warehouse_update_menu(cursor : MySQLCursor, curr_warehouse : int):
    section_open = True
    
    while section_open:
        print("==== Warehouse Update Menu ====")
        print(f"Current Warehouse: {curr_warehouse}")
        print_menu_options(Warehouse_Update_Menu_Choices)
        try:
            choice = input("Choose an option:> ")
        except:
            print("Error backing out of section")
            choice = None
            return choice
        
        if choice == Warehouse_Update_Menu_Choices.Back.value:
            print("Backing out of section")
            section_open = False

        if choice == Warehouse_Update_Menu_Choices.Update_Stock.value:
            warehouse_stock_menu(cursor, curr_warehouse)
            stock = stock_selection(cursor, curr_warehouse)
            quantChange = -10
            try:
                cursor.execute(f"CALL update_stock_quantity({stock}, {quantChange});")
            except Exception as e:
                print(f"SQL Error: {e}")
            section_open = True

        if choice == Warehouse_Update_Menu_Choices.New_Stock.value:
            pass

        if choice == Warehouse_Update_Menu_Choices.Change_Adress.value:
            pass
# Not Done
def warehouse_stock_menu(cursor : MySQLCursor, curr_warehouse : int):
    # print intro

    # print options
    print_menu_options(Warehouse_Stock_Menu_Choices)

    # loop while open
        # recieve choice

        # handle choice

        # return choice

def warehouse_menu(cursor : MySQLCursor, curr_warehouse : int):
    section_open = True

    while section_open:
        print("==== Warehouse Menu ====")
        print(f"Current warehouse: {curr_warehouse}")
        
        print_menu_options(Warehouse_Menu_Choices)

        try:
            choice = input("Choose an option:> ")
        except:
            print("\nError: Closing Menu")
            section_open = False
        
        if choice == Warehouse_Menu_Choices.Back.value:
            print("Going back")
            section_open = False

        elif choice == Warehouse_Menu_Choices.View.value:
            print("initiate view menu")
            warehouse_view_menu(cursor, curr_warehouse)
            

        elif  choice == Warehouse_Menu_Choices.Update.value:
            print("initiate update menu")
            warehouse_update_menu(cursor, curr_warehouse)
