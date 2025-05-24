import os
import dbcmd
import database

# Console
clear = lambda: print("Clear function not defined.")
if os.name == 'nt':
    clear = lambda: os.system('cls')
else:
    clear = lambda: os.system('clear')


if __name__ == "__main__":
    # Initialize the database
    db = database.Database("warehouseDatabase")

    clear()
    print("Starting Warehouse Management System...")

    while db.is_open():
        print("q - Exit")
        print("Select Mode (e / m)\n")

        mode = input("> ").lower()

        if mode == "m":
            import menu
            devmode = menu.main_menu(db)

            if devmode:
                print("Entered dev mode")
                while db.is_open():
                    try:
                        cmd_in = input("> ")
                    except:
                        print("\nError: Closing Database...")
                        db.close()
                        break

                    ret = dbcmd.exec_cmd(db, cmd_in)
                    if ret == "quit":
                        break
                    print(" ")
        elif mode == "e":
            import interface

            if db.is_open():
                interface.menu_main(db)
        elif mode == "q":
            print("Exiting...")
            break

        clear()
        
    db.close()

