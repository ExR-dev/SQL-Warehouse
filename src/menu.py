import os
from database import Database
import tableUtils
from mysql.connector.cursor import MySQLCursor
from mysql.connector import Error
from enum import Enum

class Main_Choices(Enum):
    exit = "0"
    Select_Warehouse = "1"
    Save_Database = "2"
    devmode = "dev"

class Warehouse_Menu_Choices(Enum):
    Back = "0"
    View = "1"
    Update = "2"

class Warehouse_View_Menu_Choices(Enum):
    Back = "0"
    Inventory = "1"
    Retock_Needed = "2"
    Product_quantities = "3"

class Warehouse_Update_Menu_Choices(Enum):
    Back = "0"
    Update_Stock = "1"
    New_Stock = "2"
    Change_Adress = "3"
    
class Warehouse_Stock_Menu_Choices(Enum):
    Back = "0"
    Change_Quantity = "1"
    Set_Quantity = "2"
    Change_Minimum_Quantity = "3"
    Set_Minimum_Quantity = "4"

def clear_console():
    # Clears console for both windows and linux
    os.system('cls' if os.name == "nt" else 'clear')

def print_menu_options(menu_class : Enum):
    for option in menu_class:
        print(f"{option.value}. {option.name.capitalize()}")

def get_field_names(table_description : tuple) -> list:
    # Creates a list of column names. Index 0 in column description is name of column
    field_names = [column[0] for column in table_description]
    return field_names

def main_menu(db : Database) -> bool:
    menu_open = True
    devmode = False
    cursor = db.cursor
    curr_warehouse = None


    while menu_open:
        clear_console()
        print("==== Main Menu ====")
        print(f"Current warehouse: {curr_warehouse}")
        print_menu_options(Main_Choices)
        try:
            choice = input("Choose an option:> ")
        except:
            print("\nError: Closing Menu")
            menu_open = False

        if choice == Main_Choices.exit.value:
            clear_console()
            print("Closing Menu")
            menu_open = False

        elif choice == Main_Choices.Select_Warehouse.value:
            curr_warehouse = warehouse_selection(cursor, curr_warehouse)
            if curr_warehouse is None:
                continue
            warehouse_menu(cursor, curr_warehouse)
            menu_open = True

        elif choice == Main_Choices.Save_Database.value:
            clear_console()
            print("Saving Changes")
            db.conn.commit()
            print("Database saved!")
            try:
                input("Press \"ENTER\" to continue...")
            except:
                print("\nError: Closing Menu")
                section_open = False
            continue
            

        elif choice == Main_Choices.devmode.value:
            clear_console()
            print("Entering development mode")
            menu_open = False
            devmode = True


    return devmode

def warehouse_selection(cursor : MySQLCursor, curr_warehouse : int | None) -> str:
    '''
        Prints out list of warehouses and allow user to select id coresponding to specfic warehouse,
        returns selected warehouse ID
    '''
    section_open = True
    options = []
    clear_console()

    cursor.execute("SELECT * FROM warehouse;")
    field_names = get_field_names(cursor.description)
    rows = cursor.fetchall()
    for row in rows:
        # Adds warehouse ID as a string to option list
        options.append(str(row[0]))

    while section_open:
        clear_console()
        print("======== Select a Warehouse =========")
        tableUtils.print_table(field_names, rows)
        print("q to abort selection")
        try:
            choice = input("> ")
        except:
            print("\nError closing section no warehouse will be selected")
            choice = None
            return choice

        if choice == "q":
            try:
                confirm = input("Aborting warehouse selection do you wish to keep currently selected warehouse? (y or continue)\n> ").lower()
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

def stock_selection(cursor : MySQLCursor, curr_warehouse : int | None) -> str:
    '''
        Prints out a list of stock, either for specified warehouse or all stocks,
        and allow user to select specific stock coresponding to stock ID
        Returns selected stock ID
    '''
    section_open = True
    options =[]
    if curr_warehouse is None:
        cursor.execute("SELECT * FROM Stock;")
        results = [cursor.fetchall()] # Match stored_results() style

    else:
        results = cursor.execute(f"CALL warehouse_inventory({curr_warehouse});",multi=True)

    
    for result_set in results:
        if result_set.with_rows:
            field_names = get_field_names(cursor.description)
            rows = cursor.fetchall()
            for row in rows:
                # Adds Stock ID as a string to option list
                options.append(str(row[0]))
    clear_console()

    while section_open:
        print("======== Select a Stock =========")
        tableUtils.print_table(field_names, rows)
        print("q to abort selection")
    
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
            clear_console()
            print("Unkown stock ID, try again")
            # Stay on view result untill input has been given
            try:
                input("Press \"ENTER\" to continue...")
            except:
                print("\nError: Closing Menu")
                section_open = False
            continue

    return choice

def warehouse_view_menu(cursor : MySQLCursor, curr_warehouse : int):
    section_open = True

    while section_open:
        clear_console()
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
            clear_console()
            print("==== Warehouse Inventory ====")

            try:    
                for result in cursor.execute(sql_inventory_view, multi=True):
                    if result.with_rows:
                        field_names = get_field_names(cursor.description)
                        rows = cursor.fetchall()
                        tableUtils.print_table(field_names, rows)

            except Exception as e:
                print("Error: Please Conntact system admin")
                print(f"SQL Error: {e}")

            # Stay on view result untill input has been given
            try:
                input("Press \"ENTER\" to continue...")
            except:
                print("\nError: Closing Menu")
                section_open = False

        elif choice == Warehouse_View_Menu_Choices.Retock_Needed.value:
            sql_torestock_needed =f'''CALL get_order_list({curr_warehouse});'''
            clear_console()
            print("==== Warehouse Restock List ====")

            try:    
                for result in cursor.execute(sql_torestock_needed, multi=True):
                    if result.with_rows:
                        field_names = get_field_names(cursor.description)
                        rows = cursor.fetchall()
                        tableUtils.print_table(field_names, rows)

            except Exception as e:
                print("Error: Please Conntact system admin")
                print(f"SQL Error: {e}")

            # Stay on view result untill input has been given
            try:
                input("Press \"ENTER\" to continue...")
            except:
                print("\nError: Closing Menu")
                section_open = False

        elif choice == Warehouse_View_Menu_Choices.Product_quantities.value:
            sql_total_quantity = f'''CALL total_quantity();'''
            clear_console()
            print("==== Product Quantity List ====")

            try:
                for result in cursor.execute(sql_total_quantity, multi=True):
                    if result.with_rows:
                        field_names = get_field_names(cursor.description)
                        rows = cursor.fetchall()
                        tableUtils.print_table(field_names, rows)

            except Exception as e:
                print("Error: Please Conntact system admin")
                print(f"SQL Error: {e}")

            # Stay on view result untill input has been given
            try:
                input("Press \"ENTER\" to continue...")
            except:
                print("\nError: Closing Menu")
                section_open = False

def warehouse_update_menu(cursor : MySQLCursor, curr_warehouse : int):
    section_open = True
    
    while section_open:
        clear_console()
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
            section_open = True

        if choice == Warehouse_Update_Menu_Choices.New_Stock.value:
            clear_console()
            print("Not Implemented yet")
            try:
                input("Press \"ENTER\" to continue...")
            except:
                print("\nError: Closing Menu")
                section_open = False
            continue

        if choice == Warehouse_Update_Menu_Choices.Change_Adress.value:
            clear_console()
            print("Not Implemented yet")
            try:
                input("Press \"ENTER\" to continue...")
            except:
                print("\nError: Closing Menu")
                section_open = False
            continue

def warehouse_stock_menu(cursor : MySQLCursor, curr_warehouse : int):
    section_open = True
    # loop while open
    while section_open:
        clear_console()
        # print intro
        print("==== Warehouse Stock Menu ====")
        print(f"Current Warehouse: {curr_warehouse}")
        # print options
        print_menu_options(Warehouse_Stock_Menu_Choices)

        # recieve choice
        try:
            choice = input("Choose an option:> ")
        except:
            print("Error backing out of section")
            return
        # handle choice
        if choice == Warehouse_Stock_Menu_Choices.Back.value:
            print("Backing out")
            section_open = False

        if choice == Warehouse_Stock_Menu_Choices.Change_Quantity.value:
            stock = stock_selection(cursor, curr_warehouse)
            if stock is None:
                continue

            number = False
            while not number:
                clear_console()
                print(f"Selected stock: {stock}")
                try:
                    quantity_change = input("Quantity change:> ")
                except:
                    return

                try: 
                    quantity_change = int(quantity_change)
                    number = True
                except:
                    clear_console()
                    print("Please input a whole number")
                    # Stay on view result untill input has been given
                    try:
                        input("Press \"ENTER\" to continue...")
                    except:
                        print("\nError: Closing Menu")
                        section_open = False
                    continue
                

            try:
                cursor.execute(f"CALL update_stock_quantity({stock}, {quantity_change});")
            except Exception as e:
                print(f"SQL Error: {e}")

        if choice == Warehouse_Stock_Menu_Choices.Set_Quantity.value:
            stock = stock_selection(cursor, curr_warehouse)
            if stock is None:
                continue
            
            number = False
            while not number:
                clear_console()
                print(f"Selected stock: {stock}")
                try:
                    new_quantity = input("New Quantity:> ")
                except:
                    return

                try: 
                    new_quantity = int(new_quantity)
                    number = True
                except:
                    clear_console()
                    print("Please input a whole number")
                    # Stay on view result untill input has been given
                    try:
                        input("Press \"ENTER\" to continue...")
                    except:
                        print("\nError: Closing Menu")
                        section_open = False
                    continue

            try:
                cursor.execute(f"CALL set_stock_quantity({stock}, {new_quantity});")
            except Exception as e:
                print(f"SQL Error: {e}")
        
        if choice == Warehouse_Stock_Menu_Choices.Change_Minimum_Quantity.value:
            stock = stock_selection(cursor, curr_warehouse)
            if stock is None:
                continue

            number = False
            while not number:
                clear_console()
                print(f"Selected stock: {stock}")
                try:
                    quantity_change = input("Minumum Quantity change:> ")
                except:
                    return

                try: 
                    quantity_change = int(quantity_change)
                    number = True
                except:
                    clear_console()
                    print("Please input a whole number")
                    # Stay on view result untill input has been given
                    try:
                        input("Press \"ENTER\" to continue...")
                    except:
                        print("\nError: Closing Menu")
                        section_open = False
                    continue

            try:
                cursor.execute(f"CALL update_stock_minQuantity({stock}, {quantity_change});")
            except Exception as e:
                print(f"SQL Error: {e}")

        if choice == Warehouse_Stock_Menu_Choices.Set_Minimum_Quantity.value:
            stock = stock_selection(cursor, curr_warehouse)
            if stock is None:
                continue

            number = False
            while not number:
                clear_console()
                print(f"Selected stock: {stock}")
                try:
                    new_minQuantity = input("New Minumum Quantity:> ")
                except:
                    return

                try: 
                    new_minQuantity = int(new_minQuantity)
                    number = True
                except:
                    clear_console()
                    print("Please input a whole number")
                    # Stay on view result untill input has been given
                    try:
                        input("Press \"ENTER\" to continue...")
                    except:
                        print("\nError: Closing Menu")
                        section_open = False
                    continue

            try:
                cursor.execute(f"CALL set_stock_minQuantity({stock}, {new_minQuantity});")
            except Exception as e:
                print(f"SQL Error: {e}")

def warehouse_menu(cursor : MySQLCursor, curr_warehouse : int):
    section_open = True

    while section_open:
        clear_console()
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
