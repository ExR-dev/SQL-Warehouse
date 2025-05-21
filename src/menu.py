import mysql.connector
from database import Database
# from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from mysql.connector import Error
from enum import Enum

class Main_Choices(Enum):
    exit = "0"
    warehouse_selection = "1"
    option2 = "2"
    option3 = "3"
    devmode = "dev"

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


def main_menu(db : Database):
    menu_open = True
    devmode = False
    cursor = db.cursor
    curr_warehouse = None

    print("\n==== Warehouse Inventory Main Menu ====")
    print(curr_warehouse)
    for option in Main_Choices:
        print(f"{option.value}. {option.name.capitalize()}")

    while menu_open:
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

        elif choice == Main_Choices.warehouse_selection.value:
            curr_warehouse = warehouse_menu(cursor, curr_warehouse)
            print(curr_warehouse)
            menu_open = True

    return devmode

def warehouse_menu(cursor : MySQLCursor, curr_warehouse : int | None):
    # Query the warehouse table print out as an option list move to next step in menu
    section_open = True
    options = []

    print("======== Select a Warehouse =========")
    print("q to abort selection")
    cursor.execute("SELECT * FROM warehouse;")

    
    while section_open:
        for result in cursor:
            print(result)
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
