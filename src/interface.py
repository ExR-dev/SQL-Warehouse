import os
import keyboard
import database
import dbcmd
import tableUtils

# Console
clear = lambda: print("Clear function not defined.")
if os.name == 'nt':
    clear = lambda: os.system('cls')
else:
    clear = lambda: os.system('clear')

def print_separator(separator="=", prefix="", suffix="", width=80):
    print(prefix+(separator*width)+suffix)


# User Input
def flush_input():
    """
    Clears the input buffer from keybard input. If this is not called after using the keyboard 
    module, there will likely be many unflushed inputs from interacting with the menu.
    """
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios    #for linux/unix
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

held_keys = [ 28 ] # Starting with enter pressed
key_in = None

def get_input():
    key_in = None
    keep_event = False

    while not keep_event:
        key_in = keyboard.read_event()

        # Skip key release events
        if key_in.event_type == "up":
            # Remove from held keys before skipping
            try:
                held_keys.remove(key_in.scan_code)
            except: 
                pass
            continue

        is_held = False
        try:
            held_keys.index(key_in.scan_code)
            is_held = True
        except: 
            is_held = False
        
        if is_held: 
            #continue # Skip sustained key presses
            pass 
        else:
            held_keys.append(key_in.scan_code)

        keep_event = True

    flush_input()

    match key_in.scan_code:
        case 28: # Enter
            return "select"

        case 77: # Right
            return "select"

        case 72: # Up
            return "up"

        case 80: # Down
            return "down"

        case 1: # Escape
            return "back"
        
        case 75: # Left
            return "back"
        
    return "none"


# Menu Utility
menu_chain = []
class _Break(Exception): pass

def menu_handler(db: database.Database, menu_state: dict):
    if menu_state["reprint"]:
        clear()

        # Print the menu chain
        print(" > ".join(menu_chain + [menu_state["name"]]))

        print_separator()

        desc = menu_state["desc"]
        if desc != None and desc != "":
            # Print menu description
            print(desc)
            print_separator(separator="—")

        # Print the available commands
        for option_id in range(len(menu_state["options"])):
            option = menu_state["options"][option_id]
            is_selected = (option_id == menu_state["select_id"])

            selector = "--> " if is_selected else "  "
            print(selector + option["name"])
        print_separator(suffix="\n\n")
        menu_state["reprint"] = False

    user_input = get_input()
    menu_state["reprint"] = (False if user_input == "none" else True)

    try:
        select_id = menu_state["select_id"]
        menu_options = menu_state["options"]
        options_length = len(menu_options)

        match user_input:
            case "select":
                if options_length <= select_id:
                    raise _Break()

                selected_option = menu_options[select_id]
                selected_func = selected_option["func"]
                option_params = selected_option["params"]

                menu_chain.append(menu_state["name"])
                if not selected_func(db, option_params):
                    menu_state["loop"] = False
                menu_chain.pop()

            case "up":
                if options_length <= 0:
                    raise _Break()
                
                menu_state["select_id"] = (select_id - 1) % options_length

            case "down": # Down
                if options_length <= 0:
                    raise _Break()
                
                menu_state["select_id"] = (select_id + 1) % options_length

            case "back": # Escape
                menu_state["loop"] = False
    except _Break:
        pass

def new_menu_state():
    return {
        "loop": True,
        "select_id": 0,
        "reprint": True,
        "name": "UNDEFINED",
        "desc": "",
        "options": [ ]
    }

def go_back(db: database.Database, params = None):
    return False

# Sub Menus
# View
def menu_view_products(db: database.Database, params = None):
    menu_state = new_menu_state()
    menu_state["name"] = "Products"

    # Fetch all products, along with their suppliers
    db.cursor.execute("""
    SELECT p.ID AS product_id, s.ID AS supplier_id, p.description, s.address AS supplier_address
    FROM Product p
    INNER JOIN Supplier s ON p.sup_ID = s.ID;
    """)
    field_names = [i[0] for i in db.cursor.description]
    rows = db.cursor.fetchall()

    menu_state["desc"] = tableUtils.table_to_string(field_names, rows)
    
    menu_state["options"].append({
        "name": "Back", 
        "func": go_back,
        "params": None
    })

    while menu_state["loop"]:
        menu_handler(db, menu_state)

    clear()
    return True

def menu_restock_schedule(db: database.Database, params = None):
    menu_state = new_menu_state()
    menu_state["name"] = "Restock Schedule"

    query_str = f"CALL get_order_list({params});"
    for ret in db.cursor.execute(query_str, multi=True):
        if ret.with_rows:
            field_names = [i[0] for i in ret.description]
            rows = ret.fetchall()
            menu_state["desc"] = tableUtils.table_to_string(field_names, rows)
    
    menu_state["options"].append({ 
        "name": "Back", 
        "func": go_back,
        "params": None
    })

    while menu_state["loop"]:
        menu_handler(db, menu_state)

    clear()
    return True

def menu_restock_history(db: database.Database, params = None):
    menu_state = new_menu_state()
    menu_state["name"] = "Restock History"

    # Fetch full restock history of current warehouse
    # toRestock has stock_ID, Stock has WH_ID
    # Stock has prod_ID, Product has description
    # Remove items with no dateOrdered
    db.cursor.execute(f"""
    SELECT 
        description AS product_desc, dateAdded AS date_added, dateOrdered AS date_ordered, 
        DATEDIFF(dateOrdered, dateAdded) AS days_elapsed, orderCount AS order_count
    FROM (
        SELECT r.stock_ID, p.description, r.dateAdded, r.dateOrdered, r.orderCount
        FROM ToRestock r
        INNER JOIN Stock s ON r.stock_ID = s.ID
        INNER JOIN Product p ON s.prod_ID = p.ID
        WHERE s.WH_ID = {params}
        ORDER BY r.dateAdded DESC
    ) AS subquery
    WHERE dateOrdered IS NOT NULL;
    """)

    field_names = [i[0] for i in db.cursor.description]
    rows = db.cursor.fetchall()
    menu_state["desc"] = tableUtils.table_to_string(field_names, rows)
    
    menu_state["options"].append({ 
        "name": "Back", 
        "func": go_back,
        "params": None
    })

    while menu_state["loop"]:
        menu_handler(db, menu_state)

    clear()
    return True

def menu_view_warehouse(db: database.Database, params = None):
    menu_state = new_menu_state()
    menu_state["name"] = f"{params[1]}"

    menu_state["options"].append({ 
        "name": "Stock",
        "func": menu_TODO,
        "params": None
    })

    menu_state["options"].append({
        "name": "Restock Schedule",
        "func": menu_restock_schedule,
        "params": params[0] # warehouse ID
    })

    menu_state["options"].append({ 
        "name": "Restock History",
        "func": menu_restock_history,
        "params": params[0] # warehouse ID
    })

    while menu_state["loop"]:
        menu_handler(db, menu_state)

    clear()
    return True

def menu_select_view_warehouse(db: database.Database, params = None):
    menu_state = new_menu_state()
    menu_state["name"] = "Warehouse"

    # Fetch all warehouses
    db.cursor.execute("SELECT id, address FROM warehouse;")
    rows = db.cursor.fetchall()

    # Add each warehouse as an option
    for row in rows:
        menu_state["options"].append({
            "name": f"[{row[0]}] " + row[1], # address
            "func": menu_view_warehouse,
            "params": row
        })

    while menu_state["loop"]:
        menu_handler(db, menu_state)

    clear()
    return True

def menu_view_database(db: database.Database, params = None):
    """
    Submenu for viewing data stored in the database, like seeing 
    stock counts, all stock in a warehouse, order schedule, etc.
    """
    menu_state = new_menu_state()
    menu_state["name"] = "View"
    
    menu_state["options"].append({ 
        "name": "View Warehouses", 
        "func": menu_select_view_warehouse,
        "params": None
    })

    menu_state["options"].append({ 
        "name": "View Products", 
        "func": menu_view_products,
        "params": None
    })

    while menu_state["loop"]:
        menu_handler(db, menu_state)

    clear()
    return True

# Modify
def menu_update_stock(db: database.Database, params = None):
    has_given_invalid_input = False
    has_number = False
    change = 0
    
    while not has_number:
        flush_input()
        clear()

        # Print the menu chain
        print(" > ".join(menu_chain + ["Update Stock"]))
        print_separator()
        print("Enter the change in stock quantity (positive to add, negative to remove)\n")
        print(f"Stock: {params[1]} ({params[0]})")
        print(f"Current quantity: {params[2]}")
        print(f"Minimum quantity: {params[3]}")
        print(f"Requested Change: {max(0, params[3] - params[2])}")
        print_separator()

        if has_given_invalid_input:
            print("\nInvalid input. Please enter a valid integer.\n")
        else:
            print("")
        
        try:
            change = int(input("Change: "))
            has_number = True
        except:
            has_given_invalid_input = True
        
    if change != 0:
        # Update the stock quantity in the database
        db.cursor.execute("CALL update_stock_quantity(%s, %s);", (params[0], change))
    
    clear()
    return True

def menu_select_update_stock(db: database.Database, params = None):
    menu_state = new_menu_state()
    menu_state["name"] = "Update Stock"

    while menu_state["loop"]: # Loop to update stock after returning from update_stock
        menu_state["options"] = [] # Reset options
        
        # Fetch all stocks in the warehouse
        # Sort by if the quantity is below the minimum quantity
        db.cursor.execute(f"""
        SELECT s.ID, p.description, s.quantity, s.minQuantity
        FROM stock s
        INNER JOIN product p ON s.prod_ID = p.ID
        WHERE s.WH_ID = {params}
        ORDER BY (s.quantity < s.minQuantity) DESC, s.quantity / s.minQuantity ASC;
        """)
        rows = db.cursor.fetchall()

        # Add each stock as an option
        for row in rows:
            menu_state["options"].append({
                "name": f"{row[1]} ({row[2]} / {row[3]})", # "description (quantity / minQuantity)"
                "func": menu_update_stock,
                "params": row # (stock ID, description, quantity, minQuantity)
            })

        menu_handler(db, menu_state)

    clear()
    return True

def menu_modify_warehouse(db: database.Database, params = None):
    menu_state = new_menu_state()
    menu_state["name"] = f"{params[1]}"

    menu_state["options"].append({
        "name": "Update Stock",
        "func": menu_select_update_stock,
        "params": params[0] # warehouse ID
    })

    menu_state["options"].append({
        "name": "Register Stock",
        "func": menu_TODO,
        "params": params[0] # warehouse ID
    })

    while menu_state["loop"]:
        menu_handler(db, menu_state)

    clear()
    return True

def menu_select_modify_warehouse(db: database.Database, params = None):
    menu_state = new_menu_state()
    menu_state["name"] = "Warehouse"

    # Fetch all warehouses
    db.cursor.execute("SELECT id, address FROM warehouse;")
    rows = db.cursor.fetchall()

    # Add each warehouse as an option
    for row in rows:
        menu_state["options"].append({
            "name": f"[{row[0]}] " + row[1], # address
            "func": menu_modify_warehouse,
            "params": row # (warehouse ID, address)
        })

    while menu_state["loop"]:
        menu_handler(db, menu_state)

    clear()
    return True

def menu_modify_database(db: database.Database, params = None):
    """
    Submenu for modifying data stored in the database, like adding a new supplier
    or product, (un)registering stock items, completing a restock order, etc.
    """
    menu_state = new_menu_state()
    menu_state["name"] = "Modify"

    menu_state["options"].append({
        "name": "Modify Warehouses",
        "func": menu_select_modify_warehouse,
        "params": None
    })

    while menu_state["loop"]:
        menu_handler(db, menu_state)

    # Save changes to the database
    db.commit()

    clear()
    return True

# Other
def menu_TODO(db: database.Database, params = None):
    """
    Submenu for showing that the chosen option is unimplemented
    """
    menu_state = new_menu_state()
    menu_state["name"] = "Unimplemented Option"
    menu_state["desc"] = "This option has not yet been implemented!"
    
    menu_state["options"].append({ 
        "name": "Back", 
        "func": go_back,
        "params": None
    })

    while menu_state["loop"]:
        menu_handler(db, menu_state)

    clear()
    return True

def menu_cmd(db: database.Database, params = None):
    flush_input()
    clear()
    while db.is_open():
        try:
            cmd_in = input("> ")
        except:
            print("\nError: Closing Database...")
            db.close()
            return False

        ret = dbcmd.exec_cmd(db, cmd_in)
        if ret == "quit":
            break
        print(" ")

    flush_input()
    return True

# Main Menu
def menu_main(db: database.Database, params = None):
    """
    Main menu for the simplified database interface. Uses immediate keyboard input instead of text.
    """
    menu_state = new_menu_state()
    menu_state["name"] = "Database"
    menu_state["desc"] = "Database Interface\nArrow keys can be used to navigate, select and return"
    
    menu_state["options"].append({ 
        "name": "View Database", 
        "func": menu_view_database,
        "params": None
    })

    menu_state["options"].append({
        "name": "Modify Database", 
        "func": menu_modify_database,
        "params": None
    })

    menu_state["options"].append({
        "name": "Terminal", 
        "func": menu_cmd,
        "params": None
    })

    while db.is_open() and menu_state["loop"]:
        menu_handler(db, menu_state)

    clear()
    print("Closing database interface.\n")
