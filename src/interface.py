import os
import keyboard
import database

clear = lambda: print("Clear function not defined.")
if os.name == 'nt':
    clear = lambda: os.system('cls')
else:
    clear = lambda: os.system('clear')

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


def menu_check_database(db: database.Database):
    # TODO: Add submenu for viewing data stored in the database,
    # like seeing stock counts, all stock in a warehouse, order schedule, etc.
    # Should mimic the style of menu_main() for consistency
    return

def menu_modify_database(db: database.Database):
    # TODO: Add submenu for modifying data stored in the database,
    # like adding a new supplier/product, (un)registering stock items, completing a restock order, etc.
    # Should mimic the style of menu_main() for consistency
    return

def menu_main(db: database.Database):
    """
    Main menu for the simplified database interface. Uses immediate keyboard input instead of text.
    """
    options = [
        { 
            "name": "Check Database", 
            "func": menu_check_database 
        },

        { 
            "name": "Modify Database", 
            "func": menu_modify_database 
        }
    ]

    selection_id = 0
    held_keys = [ 28 ]

    do_loop = True
    reprint = True

    while do_loop:
        if reprint:
            clear()

            # Print the available commands
            for option_id in range(len(options)):
                option = options[option_id]
                is_selected = (option_id == selection_id)

                selector = "--> " if is_selected else "   "
                print(selector + option["name"])
            print("\n")
            reprint = False

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
        reprint = True

        match key_in.scan_code:
            case 28: # Enter
                selected_func = (options[selection_id])["func"]
                selected_func(db)

            case 72: # Up
                selection_id = (selection_id - 1) % len(options)

            case 80: # Down
                selection_id = (selection_id + 1) % len(options)

            case 1: # Escape
                do_loop = False

            case _:
                # No change to terminal, no need to update text
                reprint = False

    clear()
    flush_input()
    print("Returning to command-line interface.\n")