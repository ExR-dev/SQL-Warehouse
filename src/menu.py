import mysql.connector
from database import Database
# from mysql.connector.connection import MySQLConnection
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

# def start_menu():
#     print("Establishing connection to database")
#     conn = mysql.connector.connect(
#                 host='localhost',
#                 port=3306,
#                 user='root',
#                 password='0000'
#             )
    
#     devmode = main_menu(conn)
#     print("Exiting Menu")
#     return devmode


def main_menu(db : Database) -> bool:
    menu_open = True
    devmode = False
    cursor = db.cursor
    curr_warehouse = None


    while menu_open:
        print("\n==== Warehouse Inventory Main Menu ====")
        print(curr_warehouse)
        for option in Main_Choices:
            print(f"{option.value}. {option.name.capitalize()}")

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

        if choice == "q":
            try:
                confirm = input("Aborting warehouse selection do you wish to keep currently selected warehouse? (y/n)\n> ").lower()
            except:
                print("\nError closing section no warehouse will be selected")
                choice = None
            
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

def warehouse_menu(cursor : MySQLCursor, curr_warehouse : int):
    section_open = True

    print("==== Warehouse Menu ====")
    print(f"Current warehouse: {curr_warehouse}")
    
    for option in Warehouse_Menu_Choices:
        print(f"{option.value}. {option.name.capitalize()}")
    
    while section_open:
        try:
            choice = input("Choose an option:> ")
        except:
            print("\nError: Closing Menu")
            menu_open = False
        
        if choice == Warehouse_Menu_Choices.Back.value:
            print("Going back")
            section_open = False

        elif choice == Warehouse_Menu_Choices.View.value:
            print("initiate view menu")
            

        elif  choice == Warehouse_Menu_Choices.Update.value:
            print("initiate update menu")
        
