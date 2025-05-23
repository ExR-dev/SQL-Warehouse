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

def print_separator(separator="-", prefix="", suffix=""):
    print(prefix+(separator*60)+suffix)


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
        
        # Skip sustained key presses
        if is_held: 
            continue
        
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


# Menu
# Utility
def menu_handler(db: database.Database, menu_state: dict):
    if menu_state["reprint"]:
        clear()

        desc = menu_state["desc"]
        if desc != None and desc != "":
            # Print menu description
            print_separator(suffix="")
            print(desc)
            pass

        print_separator(suffix="")
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

    match user_input:
        case "select":
            selected_option = menu_state["options"][menu_state["select_id"]]
            selected_func = selected_option["func"]
            option_params = selected_option["params"]

            if not selected_func(db, option_params):
                menu_state["loop"] = False

        case "up":
            menu_state["select_id"] = (menu_state["select_id"] - 1) % len(menu_state["options"])

        case "down": # Down
            menu_state["select_id"] = (menu_state["select_id"] + 1) % len(menu_state["options"])

        case "back": # Escape
            menu_state["loop"] = False

def new_menu_state():
    return {
        "loop": True,
        "select_id": 0,
        "reprint": True,
        "desc": "",
        "options": [ ]
    }

def go_back(db: database.Database, params = None):
    return False

# Sub Menus
def menu_TODO(db: database.Database, params = None):
    """
    Submenu for showing that the chosen option is unimplemented
    """
    menu_state = new_menu_state()
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

def menu_restock_schedule(db: database.Database, params = None):
    menu_state = new_menu_state()

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

    # Fetch full restock history of current warehouse
    # toRestock has stock_ID, Stock has WH_ID
    # Stock has prod_ID, Product has description
    # Remove items with no dateOrdered
    db.cursor.execute(f"""
    SELECT product_desc, dateAdded, dateOrdered FROM
    (SELECT r.stock_ID, p.description AS product_desc, r.dateAdded, r.dateOrdered
    FROM ToRestock r
    INNER JOIN Stock s ON r.stock_ID = s.ID
    INNER JOIN Product p ON s.prod_ID = p.ID
    WHERE s.WH_ID = {params}
    ORDER BY r.dateAdded DESC) AS subquery
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
    menu_state["desc"] = "View data associated with this warehouse\nID: " + str(params[0]) + "\nAddress: " + str(params[1])

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

def menu_view_warehouses(db: database.Database, params = None):
    menu_state = new_menu_state()
    menu_state["desc"] = "List of Warehouses"

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
    menu_state["desc"] = "View data stored in the database"
    
    menu_state["options"].append({ 
        "name": "View Warehouses", 
        "func": menu_view_warehouses,
        "params": None
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
    return menu_TODO(db)

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
